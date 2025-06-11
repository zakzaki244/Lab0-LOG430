from db import SessionLocal, init_db
from models import Store, Product

# Crée la structure si besoin
init_db()
session = SessionLocal()

# Ajoute 2 magasins si la table est vide
if session.query(Store).count() == 0:
    magasin1 = Store(name="Magasin A")
    magasin2 = Store(name="Magasin B")
    session.add_all([magasin1, magasin2])
    session.commit()
    print("Magasins créés.")

# Ajoute des produits au magasin 1
magasin1 = session.query(Store).filter_by(name="Magasin A").first()
if magasin1 and session.query(Product).count() == 0:
    produits = [
        Product(name="Bouteille d'eau", category="Boisson", price=1.5, stock=50, store=magasin1),
        Product(name="Chocolat", category="Snack", price=2.0, stock=30, store=magasin1),
    ]
    session.add_all(produits)
    session.commit()
    print("Produits ajoutés.")
else:
    print("Magasins/Produits déjà présents.")

# Ajoute des produits au magasin 2
magasin2 = session.query(Store).filter_by(name="Magasin B").first()
if magasin2 and session.query(Product).count() == 0:
    produits = [
        Product(name="Coca Cola", category="Boisson", price=1.5, stock=150, store=magasin2),
        Product(name="Sandwich", category="Snack", price=2.0, stock=400, store=magasin2),
    ]
    session.add_all(produits)
    session.commit()
    print("Produits ajoutés.")
else:
    print("Magasins/Produits déjà présents.")

session.close()
