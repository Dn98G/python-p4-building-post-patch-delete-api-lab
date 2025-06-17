#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return "<h1>Bakery GET-POST-PATCH-DELETE API</h1>"


# GET all bakeries
@app.route("/bakeries")
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)


# GET single bakery by ID
@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)
    return make_response(bakery.to_dict(), 200)


# GET baked goods sorted by price (descending)
@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response([bg.to_dict() for bg in baked_goods_by_price], 200)


# GET most expensive baked good
@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    return make_response(most_expensive.to_dict(), 200)


# ✅ CREATE a new baked good
@app.route("/baked_goods", methods=["POST"])
def create_baked_good():
    name = request.form.get("name")
    price = request.form.get("price")
    bakery_id = request.form.get("bakery_id")

    if not name or not price or not bakery_id:
        return make_response({"error": "Missing form data."}, 400)

    baked_good = BakedGood(name=name, price=float(price), bakery_id=int(bakery_id))
    db.session.add(baked_good)
    db.session.commit()

    return make_response(baked_good.to_dict(), 201)


# UPDATE bakery name
@app.route("/bakeries/<int:id>", methods=["PATCH"])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response({"error": "Bakery not found."}, 404)

    name = request.form.get("name")
    if name:
        bakery.name = name
        db.session.commit()

    return make_response(bakery.to_dict(), 200)


# ✅ DELETE a baked good
@app.route("/baked_goods/<int:id>", methods=["DELETE"])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return make_response({"error": "Baked good not found."}, 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response({"message": "Baked good deleted successfully."}, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
