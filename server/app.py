#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, json
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# GET /restaurants
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    data = [r.to_dict(only=("id", "name", "address")) for r in restaurants]
    return make_response(json.dumps(data), 200, {"Content-Type": "application/json"})

# GET /restaurants/<id>
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant_by_id(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return make_response(json.dumps({"error": "Restaurant not found"}), 404,
                             {"Content-Type": "application/json"})
    data = restaurant.to_dict(only=("id", "name", "address", "restaurant_pizzas"))
    return make_response(json.dumps(data), 200, {"Content-Type": "application/json"})

# DELETE /restaurants/<id>
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return make_response(json.dumps({"error": "Restaurant not found"}), 404,
                             {"Content-Type": "application/json"})
    db.session.delete(restaurant)
    db.session.commit()
    return make_response("", 204)

# GET /pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    data = [piz.to_dict(only=("id", "name", "ingredients")) for piz in pizzas]
    return make_response(json.dumps(data), 200, {"Content-Type": "application/json"})

# POST /restaurant_pizzas
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        rp = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(rp)
        db.session.commit()
        return make_response(json.dumps(rp.to_dict()), 201, {"Content-Type": "application/json"})
    except ValueError:
        # Test responses
        return make_response(json.dumps({"errors": ["validation errors"]}), 400,
                             {"Content-Type": "application/json"})
    except Exception:
        return make_response(json.dumps({"errors": ["validation errors"]}), 400,
                             {"Content-Type": "application/json"})

if __name__ == "__main__":
    app.run(port=5555, debug=True)
