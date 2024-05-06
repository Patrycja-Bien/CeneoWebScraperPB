from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/')
@app.route('/name/<name>')
def name(name):
    return f"Hello, {name}!"

@app.route('/extract')
def extract():
    return render_template("extract.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/product_id')
def products():
    return render_template("product.html", product_id=product_id)

@app.route('/about')
def extract():
    return render_template("about.html")

#Dorobić block content do każdej strony
#Zrobić header i footer w base.html, zgodnie z wymaganiami