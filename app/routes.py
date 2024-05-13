from app import app
from flask import render_template, request, redirect, url_for

@app.route('/') #dekorator
def index():
    return render_template("index.html")

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method=="POST":
        product_id = request.form.get("product_id")
        return redirect(url_for("product", product_id = product_id))
    return render_template("extract.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html", product_id=product_id)

@app.route('/about')
def about():
    return render_template("about.html")