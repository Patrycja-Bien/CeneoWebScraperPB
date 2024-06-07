from app import app
from flask import render_template, request, redirect, url_for, send_file
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import json
import os
import io
from . import utils

@app.route('/') #dekorator
def index():
    return render_template("index.html")

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method=="POST":
        product_id = request.form.get("product_id")
        url = f"https://www.ceneo.pl/{product_id}"
        response = requests.get(url)
        if response.status_code == requests.codes['ok']:
            page_dom = BeautifulSoup(response.text, "html.parser")
            opinions_count = utils.extract(page_dom, "a.product-review__link > span")
            if opinions_count:
                product_name = utils.extract(page_dom,"h1.product-top__product-info__name")
                all_opinions = []
                while(url):
                    response = requests.get(url)
                    page_dom = BeautifulSoup(response.text, "html.parser")
                    opinions = page_dom.select("div.js_product-review")
                    for opinion in opinions:
                        single_opinion = {
                            key: utils.extract(opinion, *value)
                                for key, value in utils.selectors.items()
                            }
                        all_opinions.append(single_opinion)
                    try:
                        url = "https://www.ceneo.pl/"+page_dom.select_one("a.pagination__next")["href"].strip()
                    except TypeError:
                        url = None
                if not os.path.exists("app/opinions"):
                    os.makedirs("app/opinions")
                with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
                    json.dump(all_opinions, jf, indent = 4, ensure_ascii = False)
                opinions = pd.DataFrame.from_dict(all_opinions)
                opinions.stars = opinions.stars.apply(lambda s: s.split("/")[0].replace(",",".")).astype(float)
                opinions.recommendations = opinions.recommendations.apply(lambda r: "Brak rekomendacji" if r is None else r)    
                stats = {
                    "opinions_id": product_id,
                    "product_name": product_name,
                    "opinions_count" : opinions.shape[0],
                    "pros_count": int(opinions.pros.apply(lambda p: None if not p else p).count()),
                    "cons_count": int(opinions.cons.apply(lambda c: None if not c else c).count()),
                    "average_stars": opinions.stars.mean(),
                    "stars_distribution": opinions.stars.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value = 0).to_dict(),
                    "recommendations_distribution": opinions.recommendations.value_counts(dropna = False).reindex(["Polecam","Brak rekomendacji","Nie polecam"], fill_value = 0).to_dict()
                }
                if not os.path.exists("app/products"):
                    os.makedirs("app/products")
                with open(f"app/products/{product_id}.json", "w", encoding="UTF-8") as jf:
                    json.dump(stats, jf, indent = 4, ensure_ascii = False)
                return redirect(url_for("product", product_id = product_id))
            return render_template("extract.html", error = "Podany produkt nie ma żadnych opinii")
        return  render_template("extract.html", error = "Produkt o podanym kodzie nie istnieje")
    return render_template("extract.html")

@app.route('/products')
def products():
    products_list = [filename.split(".")[0] for filename in os.listdir("app/opinions")]
    products = []
    for product_id in products_list:
        with open(f"app/products/{product_id}.json", "r", encoding="UTF-8") as jf:
            products.append(json.load(jf))
    return render_template("products.html", products=products)

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html", product_id=product_id)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/charts/<product_id>')
def charts(product_id):
    return render_template("charts.html", product_id=product_id)

@app.route('/product/download_json/<product_id>')
def download_json(product_id):
    return send_file(f"opinions/{product_id}.json", "text/json", as_attachment = True)

@app.route('/product/download_csv/<product_id>')
def download_csv(product_id):
    opinions = pd.read_json(f"app/opinions/{product_id}.json")
    opinions.stars = opinions.stars.apply(lambda s: "'"+s)
    buffer = io.BytesIO(opinions.to_csv(sep =";",decimal =",", index = False, quotechar='"').encode())
    return send_file(buffer, "text/csv", as_attachment = True, download_name = f"{product_id}.csv")

@app.route('/product/download_xlsx/<product_id>')
def download_xlsx(product_id):
    opinions = pd.read_json(f"app/data/opinions/{product_id}.json")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        opinions.to_excel(writer, index=False)
    buffer.seek(0)
    return send_file(buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", as_attachment=True, download_name=f"{product_id}.xlsx")

