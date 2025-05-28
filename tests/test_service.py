
import pytest
from db   import Base, engine, SessionLocal, init_db
from dao  import DAO
from service import Service
from models import Product

@pytest.fixture(autouse=True)
def setup_memory_db(monkeypatch):
    # on force DATABASE_URL sur SQLite in-memory
    # (avant que SessionLocal soit instancié dans db.py)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    # ré-crée engine et SessionLocal avec le nouveau URL
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_stock_and_search():
    session = SessionLocal()
    # on insère deux produits
    p1 = Product(name="Chocolat", category="Alimentation", price=2.5, stock=10)
    p2 = Product(name="Stylo",     category="Papeterie",   price=1.2, stock=5)
    session.add_all([p1, p2])
    session.commit()

    svc = Service()
    # stock()
    all_prod = svc.stock()
    assert len(all_prod) == 2
    # search par nom partiel
    choc = svc.search("Choco")
    assert len(choc) == 1 and choc[0].name == "Chocolat"
    # search par catégorie
    pap = svc.search("Papeterie")
    assert pap and pap[0].category == "Papeterie"
    session.close()

def test_sale_and_refund():
    svc = Service()
    session = SessionLocal()
    # ajouter un produit pour la vente
    p = Product(name="Café", category="Boissons", price=3.0, stock=3)
    session.add(p)
    session.commit()
    session.close()

    # on vend 2 cafés
    sale_id = svc.sale([(p.id, 2)])
    assert isinstance(sale_id, int)

    # stock mis à jour
    remaining = svc.stock()
    assert next(prod for prod in remaining if prod.id == p.id).stock == 1

    # on annule la vente
    svc.refund(sale_id)
    after = svc.stock()
    assert next(prod for prod in after if prod.id == p.id).stock == 3
