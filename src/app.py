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

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    results = []
    if request.method == "POST":
        term = request.form["term"]
        results = svc.search(term)
    return render_template("search.html", results=results)

@app.route("/stock")
@login_required
def stock():
    produits = svc.stock()
    return render_template("stock.html", produits=produits)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
