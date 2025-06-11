from db import SessionLocal, init_db
from models import Product

# Initialise les tables si besoin
init_db()
session = SessionLocal()

# Quelques exemples de produits à ajouter :
products = [
    Product(name="Bouteille d'eau", category="Boisson", price=1.5, stock=50),
    Product(name="Chocolat", category="Snacks", price=2.0, stock=100),
    Product(name="Pomme", category="Fruit", price=0.8, stock=70)
]

# Ajoute les produits si la table est vide
if session.query(Product).count() == 0:
    session.add_all(products)
    session.commit()
    print("Produits ajoutés !")
else:
    print("Produits déjà présents.")

session.close()
