import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {col.name: getattr(self, col.name)
                for col in self.__table__.columns}


all_cafes = db.session.query(Cafe).all()
random_id = random.randint(0, len(all_cafes))


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def random_coffee():
    random_cafe = Cafe.query.get(random_id)
    return jsonify(random_cafe.to_dict()), 200


@app.route("/all")
def all():
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes]), 200


@app.route("/search")
def search():
    loc = request.args.get("loc")
    cafe_location = Cafe.query.filter_by(location=loc).first()
    print(cafe_location)
    if not cafe_location:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
    else:
        return jsonify(cafe=cafe_location.to_dict()), 200


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_new_cafe():
    new_cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("loc"),
        seats=request.args.get("seats"),
        has_toilet=bool(request.args.get("toilet")),
        has_wifi=bool(request.args.get("wifi")),
        has_sockets=bool(request.args.get("sockets")),
        can_take_calls=bool(request.args.get("calls")),
        coffee_price=request.args.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."}), 200


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe_to_update = Cafe.query.get(cafe_id)
    if not cafe_to_update:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404
    else:
        cafe_to_update.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    api_key = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
        return jsonify(error={"Forbidden": "Please verify your API key is valid."}), 403
    else:
        cafe_to_delete = Cafe.query.get(cafe_id)
        if not cafe_to_delete:
            return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404
        else:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe."}), 200


if __name__ == "__main__":
    app.run(debug=True)
