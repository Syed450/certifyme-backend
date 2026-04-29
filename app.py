from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- MODELS --------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer)

# -------------------- ROUTES --------------------

# Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"error": "User already exists"}), 400

    user = User(
        full_name=data.get("full_name"),
        email=data["email"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data.get("email")).first()

    if not user or user.password != data.get("password"):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user_id": user.id})


# Add Opportunity
@app.route("/opportunity", methods=["POST"])
def add_opportunity():
    data = request.json

    opp = Opportunity(
        name=data.get("name"),
        category=data.get("category"),
        duration=data.get("duration"),
        start_date=data.get("start_date"),
        description=data.get("description"),
        user_id=data.get("user_id")
    )

    db.session.add(opp)
    db.session.commit()

    return jsonify({"message": "Opportunity added"})


# View Opportunities
@app.route("/opportunity/<int:user_id>", methods=["GET"])
def get_opportunities(user_id):
    opps = Opportunity.query.filter_by(user_id=user_id).all()

    result = []
    for o in opps:
        result.append({
            "id": o.id,
            "name": o.name,
            "category": o.category,
            "duration": o.duration,
            "start_date": o.start_date,
            "description": o.description
        })

    return jsonify(result)


# -------------------- RUN --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)