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
else:
    magasin1 = session.query(Store).filter_by(name="Magasin A").first()
    magasin2 = session.query(Store).filter_by(name="Magasin B").first()

# Ajoute des produits **si la table est vide**
if session.query(Product).count() == 0:
    produits = [
        Product(name="Bouteille d'eau", category="Boisson", price=1.5, stock=50, store=magasin1),
        Product(name="Chocolat", category="Snack", price=2.0, stock=30, store=magasin1),
        Product(name="Coca Cola", category="Boisson", price=1.5, stock=150, store=magasin2),
        Product(name="Sandwich", category="Snack", price=2.0, stock=400, store=magasin2),
    ]
    session.add_all(produits)
    session.commit()
    print("Produits ajoutés.")
else:
    print("Magasins/Produits déjà présents.")

session.close()
