from app import db
from flask_login import UserMixin

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, unique=True)
    description = db.Column(db.String(500))
    genre = db.Column(db.String(50))
    difficulty = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    image = db.Column(db.String(200))
    price = db.Column(db.Float)

class Customers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(50))
    baskets = db.relationship('Baskets', backref='customers', lazy=True)
    orders = db.relationship('Orders', backref='customers', lazy=True)

class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Products', backref='basket_items')

class Baskets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    items = db.relationship('BasketItem', backref='basket', lazy=True)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))
    basket = db.relationship('Baskets', backref='orders', lazy=True)
    order_date = db.Column(db.Date)
    status = db.Column(db.String(50))

