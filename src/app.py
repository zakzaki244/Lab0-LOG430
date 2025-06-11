from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from service import Service

app = Flask(__name__)
app.secret_key = "secret"

svc = Service()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Veuillez vous connecter.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        role = request.form.get("role", "")
        if username and role:
            session["username"] = username
            session["role"] = role
            flash(f"Connecté en tant que {role} ({username})")
            return redirect(url_for("index"))
        else:
            message = "Veuillez remplir tous les champs"
    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    flash("Déconnecté")
    return redirect(url_for("login"))

@app.route("/magasins")
def magasins():
    from db import SessionLocal
    from models import Store
    session = SessionLocal()
    magasins = session.query(Store).all()
    session.close()
    return render_template("magasins.html", magasins=magasins)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    results = []
    if request.method == "POST":
        term = request.form["term"]
        results = svc.search(term)
    return render_template("search.html", results=results)

@app.route("/store/<int:store_id>/stock")
def store_stock(store_id):
    from db import SessionLocal
    from models import Store, Product
    session = SessionLocal()
    store = session.query(Store).get(store_id)
    produits = session.query(Product).filter_by(store_id=store_id).all()
    session.close()
    return render_template("stock.html", store=store, products=produits)


@app.route("/sale", methods=["GET", "POST"])
@login_required
def sale():
    produits = svc.stock()
    message = ""
    if request.method == "POST":
        cart = []
        for produit in produits:
            qte = request.form.get(f"qte_{produit.id}", "0")
            try:
                qte = int(qte)
            except ValueError:
                qte = 0
            if qte > 0:
                if qte > produit.stock:
                    message = f"Stock insuffisant pour {produit.name}"
                    return render_template("sale.html", produits=produits, message=message)
                cart.append((produit.id, qte))
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

@app.route("/refund", methods=["GET", "POST"])
@login_required
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

@app.route("/rapport")
@login_required
def rapport():
    if session.get("role") != "gestionnaire":
        flash("Accès réservé aux gestionnaires de la maison mère.")
        return redirect(url_for("index"))

    from db import SessionLocal
    from models import Store, Product, Sale, SaleItem
    session_db = SessionLocal()
    
    # Ventes par magasin
    magasins = session_db.query(Store).all()
    ventes_par_magasin = {}
    produits_vendus = {}

    for magasin in magasins:
        ventes = (
            session_db.query(Sale)
            .join(SaleItem)
            .join(Product)
            .filter(Product.store_id == magasin.id)
            .all()
        )
        ventes_par_magasin[magasin.name] = len(ventes)
        # Récupérer produits les plus vendus
        items = (
            session_db.query(Product.name, SaleItem.quantity)
            .join(SaleItem, Product.id == SaleItem.product_id)
            .filter(Product.store_id == magasin.id)
            .all()
        )
        produits_vendus[magasin.name] = items

    # Stock restant par magasin
    stocks = {}
    for magasin in magasins:
        produits = session_db.query(Product).filter_by(store_id=magasin.id).all()
        stocks[magasin.name] = [(p.name, p.stock) for p in produits]

    session_db.close()
    return render_template(
        "rapport.html",
        ventes_par_magasin=ventes_par_magasin,
        produits_vendus=produits_vendus,
        stocks=stocks,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
