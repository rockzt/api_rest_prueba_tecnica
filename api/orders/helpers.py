from . import models
from datetime import datetime, timedelta
from functools import wraps
from flask import request, make_response
import jwt  # Importin JWt library (for token)
from werkzeug.security import generate_password_hash, check_password_hash  # Security tool for encrypting passwords
from api.config import Config
from api.db import  db


def build_order(client, articles_data):
    return models.Order(
        client_name=client,
        subtotal=_calculate_subtotal(articles_data),
        iva=_calculate_iva(articles_data),
        total=_calculate_total(articles_data),
        created_at=datetime.now()
    )


def build_article(article_data):
    return models.Article(
        article_name=article_data.get('article_name'),
        price=article_data.get('price'),
        quantity=article_data.get('quantity')
    )


def build_get_order(order):
    return {
        'id': order.id,
        'client_name': order.client_name,
        'subtotal': order.subtotal,
        'iva': order.iva,
        'total': order.total,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'cancel_at': order.cancel_at.strftime('%Y-%m-%d %H:%M:%S') if order.cancel_at else None,
        'articles': [
            {
                'article_name': article.article_name,
                'price': article.price,
                'quantity': article.quantity
            }
            for article in order.articles
        ]
    }



# Token Validation
def token_required(func):
    @wraps(func)  # Mandatory user this decorator, flask do not accept simple decorators
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        prefix = 'Bearer '
        if not authorization:
            return {"detail": "Missing Authorization header"}, 401

        if not authorization.startswith(prefix):
            return {"detail": "Invalid Token Prefix"}, 401

        print(f"Authorization Value: {authorization}")
        token = authorization.split(" ")[1]

        if not token:
            return {"detail": "Missing Token"}, 401

        # Validates token still valid
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"detail" : "Token Expired"}, 401
        except jwt.exceptions.InvalidTokenError:
            return {"detail" : "Invalid Token"}, 401

        request.user = db.session.execute(
            db.select(models.User).where(models.User.id == payload["sub"])
        ).scalar_one()
        return func(*args, **kwargs)

    return wrapper


# Private Methods
def _calculate_subtotal(articles_data):
    sum_subtotal = 0
    for article  in articles_data:
        price = article.get('price')
        sum_subtotal += price
    return sum_subtotal


def _calculate_iva(articles_data):
    subtotal = _calculate_subtotal(articles_data)
    iva = subtotal * 0.16
    truncated_iva = int(iva * 100) / 100
    return truncated_iva


def _calculate_total(articles_data):
    subtotal = _calculate_subtotal(articles_data)
    iva = _calculate_iva(articles_data)
    total = subtotal + iva
    return total