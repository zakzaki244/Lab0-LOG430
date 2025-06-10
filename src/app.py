from flask import Flask, render_template, request, redirect, url_for, flash
from service import Service

app = Flask(__name__)
app.secret_key = "dev"   

svc = Service()

@app.route("/")
def home():
    return render_template("index.html")


#Route /search : formulaire de recherche produit 
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        term = request.form.get("term")
        results = svc.search(term)
    return render_template("search.html", results=results)

#Route /stock : liste du stock

#Route /sale/new : formulaire pour une nouvelle vente

#Route /sale/delete : formulaire d’annulation de vente



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
