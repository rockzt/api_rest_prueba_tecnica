from api.db import db
# Used to generated specific columns used by the model
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
# Importing datatypes for creating Model
from sqlalchemy import Integer, String, DateTime, ForeignKey, Double
import datetime


# Inheriting from db model created by SQLAlchemy
class User(db.Model):
    """User Object"""
    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(255), nullable=False)
    last_name = mapped_column(String(255), nullable=True)
    email = mapped_column(String(100), unique=True)
    password = mapped_column(String(255), nullable=False)


# Association table
order_article_m2m = db.Table(
    "order_article",
    db.Column("order_id", Integer, db.ForeignKey("order.id")),
    db.Column("article_id", Integer, db.ForeignKey("article.id")),
)


class Order(db.Model):

    id = mapped_column(Integer, primary_key=True)
    client_name = mapped_column(String(255), nullable=False)
    articles = db.relationship(
        "Article", secondary=order_article_m2m, back_populates="orders"
    )
    subtotal = mapped_column(Double, nullable=False)
    iva = mapped_column(Double, nullable=False)
    total = mapped_column(Double, nullable=False)
    created_at = mapped_column(DateTime, default=db.func.datetime)
    cancel_at = mapped_column(DateTime)


class Article(db.Model):

    id = mapped_column(Integer, primary_key=True)
    article_name = mapped_column(String(255), nullable=False)
    price = mapped_column(Double, nullable=False)
    quantity = mapped_column(Integer, nullable=False)

    orders = db.relationship(
        "Order", secondary=order_article_m2m, back_populates="articles"
    )