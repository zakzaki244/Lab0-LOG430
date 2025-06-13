from flask import Blueprint, jsonify, request
from models import Product, Store, Sale
from db import SessionLocal
from service import Service

api = Blueprint('api', __name__, url_prefix='/api')

# -------- PRODUITS --------
@api.route("/products", methods=["GET"])
def get_products():
    session = SessionLocal()
    produits = session.query(Product).all()
    data = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "stock": p.stock,
            "store_id": p.store_id
        }
        for p in produits
    ]
    session.close()
    return jsonify(data)

@api.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    session = SessionLocal()
    produit = session.query(Product).get(pid)
    if not produit:
        return jsonify({"error": "Produit non trouvé"}), 404
    data = {
        "id": produit.id,
        "name": produit.name,
        "category": produit.category,
        "price": produit.price,
        "stock": produit.stock,
        "store_id": produit.store_id
    }
    session.close()
    return jsonify(data)

@api.route("/products", methods=["POST"])
def create_product():
    session = SessionLocal()
    data = request.get_json()
    produit = Product(
        name=data["name"],
        category=data.get("category", ""),
        price=float(data["price"]),
        stock=int(data["stock"]),
        store_id=int(data["store_id"])
    )
    session.add(produit)
    session.commit()
    session.close()
    return jsonify({"success": True, "id": produit.id}), 201

@api.route("/products/<int:pid>", methods=["PUT", "PATCH"])
def update_product(pid):
    session = SessionLocal()
    produit = session.query(Product).get(pid)
    if not produit:
        session.close()
        return jsonify({"error": "Produit non trouvé"}), 404
    data = request.get_json()
    produit.name = data.get("name", produit.name)
    produit.category = data.get("category", produit.category)
    produit.price = float(data.get("price", produit.price))
    produit.stock = int(data.get("stock", produit.stock))
    produit.store_id = int(data.get("store_id", produit.store_id))
    session.commit()
    session.close()
    return jsonify({"success": True})

@api.route("/products/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    session = SessionLocal()
    produit = session.query(Product).get(pid)
    if not produit:
        session.close()
        return jsonify({"error": "Produit non trouvé"}), 404
    session.delete(produit)
    session.commit()
    session.close()
    return jsonify({"success": True})

# -------- MAGASINS --------
@api.route("/magasins", methods=["GET"])
def get_magasins():
    session = SessionLocal()
    magasins = session.query(Store).all()
    data = [{"id": m.id, "name": m.name} for m in magasins]
    session.close()
    return jsonify(data)

@api.route("/magasins/<int:mid>", methods=["GET"])
def get_magasin(mid):
    session = SessionLocal()
    magasin = session.query(Store).get(mid)
    if not magasin:
        session.close()
        return jsonify({"error": "Magasin non trouvé"}), 404
    data = {
        "id": magasin.id,
        "name": magasin.name,
        "produits": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "stock": p.stock
            }
            for p in magasin.products
        ]
    }
    session.close()
    return jsonify(data)

# --------- VENTES/RAPPORT ---------
@api.route("/ventes", methods=["GET"])
def get_ventes():
    session = SessionLocal()
    ventes = session.query(Sale).all()
    data = []
    for v in ventes:
        data.append({
            "id": v.id,
            "timestamp": v.timestamp.isoformat(),
            "items": [
                {"product_id": item.product_id, "quantity": item.quantity}
                for item in v.items
            ]
        })
    session.close()
    return jsonify(data)



