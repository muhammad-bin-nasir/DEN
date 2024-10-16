from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production

# Initialize SQLAlchemy and JWTManager
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Create User and Product models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials!"}), 401

    token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(hours=1))
    return jsonify({"token": token}), 200

# Create a Product (Protected)
@app.route('/product', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created successfully!"}), 201

# Get a Product by ID
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"id": product.id, "name": product.name, "description": product.description, "price": product.price})

# Update a Product by ID (Protected)
@app.route('/product/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    db.session.commit()

    return jsonify({"message": "Product updated successfully!"})

# Delete a Product by ID (Protected)
@app.route('/product/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully!"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)