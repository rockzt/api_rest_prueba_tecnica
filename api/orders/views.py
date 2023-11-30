from . import api_blueprint
from . import models
from . import helpers
from datetime import datetime, timedelta
from flask import request
import jwt  # Importin JWt library (for token)
# Security tool for encrypting passwords
from werkzeug.security import generate_password_hash, check_password_hash
from api.db import db
from api.config import Config


# Check Running App
@api_blueprint.route("/health", methods=["GET"])
def health():
    return "Project Working Correctly from API from orders !!!"


@api_blueprint.route("/protected", methods=["GET"])
@helpers.token_required
def protected():
    return "Protected View!!!"


# Api endpoints
@api_blueprint.route('/order', methods=['POST'])
@helpers.token_required
def create_order():
    try:
        # Verify that the request contains JSON data
        if not request.is_json:
            return {'error': 'Invalid content type. Must be JSON'}, 400

        # Assuming JSON data is sent in the request
        data = request.get_json()
        # Validating required data
        if 'client_name' not in data or 'articles' not in data:
            return {'error': 'Missing required fields'}, 400
        # Extract client information
        client = data.get('client_name')
        # Extract articles information
        articles_data = data.get('articles')
        # Checking if the list of articles is not empty
        if not articles_data:
            return {'error': 'No articles provided'}, 400
        # Building order object
        order = helpers.build_order(client, articles_data)

        for article_data in articles_data:

            # Validate article data
            if ('article_name' not in article_data or 'price' not in article_data
                    or 'quantity' not in article_data):
                return {'error': 'Invalid article data'}, 400

            # Validate quantity is a positive integer
            try:
                quantity = int(article_data.get('quantity'))
                if quantity <= 0:
                    return {'error': 'Invalid quantity'}, 400
            except ValueError:
                return {'error': 'Quantity must be a positive integer'}, 400

            # Validate price is a positive number
            try:
                price = float(article_data['price'])
                if price <= 0:
                    return {'error': 'Invalid price, can not be 0'}, 400
            except ValueError:
                return {'error': 'Price must be a positive number'}, 400

            article = helpers.build_article(article_data)

            order.articles.append(article)

        db.session.add(order)
        db.session.commit()
        return {'message': 'Order created successfully'}, 201

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500


@api_blueprint.route('/order', methods=['GET'])
def get_all_orders():
    try:
        # Query all orders with their related products
        orders_query = models.Order.query
        # Check if 'created_at' parameter is provided in the request
        created_at_filter = request.args.get('created_at')
        if created_at_filter:
            # Filter orders created after the specified timestamp
            orders_query = orders_query.filter(
                models.Order.created_at >= created_at_filter)
        # Check if 'cancel_at' parameter is provided in the request
        cancel_at_filter = request.args.get('cancel_at')
        if cancel_at_filter:
            # Filter orders canceled after the specified timestamp
            orders_query = orders_query.filter(
                models.Order.cancel_at >= cancel_at_filter)

        # Get the filtered orders
        orders = orders_query.all()
        # Check if there are no orders
        if not orders:
            return {'message': 'No orders found'}, 404
        # Serialize the orders and related products into a JSON response
        orders_data = []
        orders_count = 0
        for order in orders:
            orders_count += 1
            order_data = helpers.build_get_order(order)
            orders_data.append(order_data)
        return {'orders': orders_data, 'orders_qty': orders_count}, 200
    except Exception as e:
        return {'error': str(e)}, 500


@api_blueprint.route('/order/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    try:
        # Check if order_id is non-positive
        if order_id <= 0:
            return {'message': 'Invalid order ID'}, 400
        # Query the order by ID
        order = models.Order.query.get(order_id)
        # Check order exist
        if not order:
            return {'message': 'Order not found'}, 404
        # Serialize the order and its related products into a JSON response
        order_data = helpers.build_get_order(order)
        return {'order': order_data}

    except Exception as e:
        return {'error': str(e)}, 500


@api_blueprint.route('/order/<int:order_id>/cancel', methods=['PUT'])
@helpers.token_required
def cancel_order(order_id):
    try:
        # Check if order_id is non-positive
        if order_id <= 0:
            return {'message': 'Invalid order ID'}, 400
        # Query the order by ID
        order = models.Order.query.get(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        # Check if the order is already canceled
        if order.cancel_at:
            return {'message': 'Order is already canceled'}, 400
        # Cancel the order and update the cancel_at timestamp
        order.cancel_at = datetime.now()
        db.session.commit()
        return {'message': 'Order canceled successfully'}

    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500


# Create User
@api_blueprint.route("/signup/", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return {"detail": "email required"}, 400
        # Creating DB connection
    user_exist = db.session.execute(
        # Select from User model (select * from user where email = user_exist
        db.select(models.User).where(models.User.email == email)
    ).scalar_one_or_none()
    if user_exist:
        return {"detail": "Email already taken"}, 400

    passowrd = data.get("password")
    user = models.User(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=email,
        password=generate_password_hash(passowrd),  # Encrypting password
    )
    db.session.add(user)
    db.session.commit()
    return {"detail": "User created successfully"}, 201


# Get Token
@api_blueprint.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"detail": "Missing email or password"}, 400

    user = db.session.execute(
        db.select(models.User).where(models.User.email == email)
    ).scalar_one_or_none()

    # Checking if password is correct and also if user exist
    if not user or not check_password_hash(user.password, password):
        return {"detail": "Invalid email or password"}, 401

    # Specify subject and expire date on JWT Token
    # Token will expire in 30 min
    token = jwt.encode(
        {
            "sub": user.id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        Config.SECRET_KEY,
    )
    return {"token": token}
