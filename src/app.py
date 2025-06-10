from flask import Flask, render_template, request, redirect, url_for, flash
from service import Service

app = Flask(__name__)
app.secret_key = "dev"   

svc = Service()

@app.route("/")
def index():
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
@app.route("/stock")
def stock():
    produits = svc.stock()
    return render_template("stock.html", produits=produits)

#Route /sale/new : formulaire pour une nouvelle vente
@app.route("/sale", methods=["GET", "POST"])
def sale():
    produits = svc.stock()
    message = ""
    if request.method == "POST":
        cart = []
        for pid in produits:
            qte = request.form.get(f"qte_{pid.id}", "0")
            try:
                qte = int(qte)
            except ValueError:
                qte = 0
            if qte > 0:
                cart.append((pid.id, qte))
        if cart:
            try:
                sale_id = svc.sale(cart)
                flash(f"Vente #{sale_id} enregistrée !")
                return redirect(url_for("sale"))
            except Exception as e:
                message = str(e)
        else:
            message = "Aucun article sélectionné."
    return render_template("sale.html", produits=produits, message=message)


#Route /sale/refund : formulaire d’annulation de vente
@app.route("/refund", methods=["GET", "POST"])
def refund():
    message = ""
    if request.method == "POST":
        sid = request.form.get("sale_id", "")
        try:
            svc.refund(int(sid))
            flash(f"Vente #{sid} annulée.")
            return redirect(url_for("refund"))
        except Exception as e:
            message = str(e)
    return render_template("refund.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

