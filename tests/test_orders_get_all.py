import unittest
import json
from flask import Flask
from api import create_app, db
from datetime import datetime
from api.orders import models


class OrdersTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_all_orders(self):
        # Create a sample order in the database
        with self.app.app_context():
            order = models.Order(
                client_name='John Doe',
                subtotal=100.0,
                iva=16.0,
                total=116.0,
                created_at=datetime(2023, 1, 1, 12, 0, 0),
                cancel_at=None
            )
            db.session.add(order)
            db.session.commit()

        # Send a GET request to the orders/order endpoint
        response = self.client.get('orders/order')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json)
        self.assertEqual(len(response.json['orders']), 1)
        self.assertEqual(response.json['orders_qty'], 1)

    def test_get_all_orders_with_created_at_filter(self):
        # Create sample orders in the database with different created_at timestamps
        with self.app.app_context():
            order1 = models.Order(
                client_name='John Doe',
                subtotal=100.0,
                iva=16.0,
                total=116.0,
                created_at=datetime(2023, 1, 1, 12, 0, 0),
                cancel_at=None
            )
            order2 = models.Order(
                client_name='Jane Doe',
                subtotal=150.0,
                iva=24.0,
                total=174.0,
                created_at=datetime(2023, 1, 2, 12, 0, 0),
                cancel_at=None
            )
            db.session.add_all([order1, order2])
            db.session.commit()

        # Send a GET request to the orders/order endpoint with a created_at filter
        response = self.client.get('orders/order?created_at=2023-01-02T00:00:00')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json)
        self.assertEqual(len(response.json['orders']), 1)
        self.assertEqual(response.json['orders_qty'], 1)

    def test_get_all_orders_with_cancel_at_filter(self):
        # Create sample orders in the database with different cancel_at timestamps
        with self.app.app_context():
            order1 = models.Order(
                client_name='John Doe',
                subtotal=100.0,
                iva=16.0,
                total=116.0,
                created_at=datetime(2023, 1, 1, 12, 0, 0),
                cancel_at=None
            )
            order2 = models.Order(
                client_name='Jane Doe',
                subtotal=150.0,
                iva=24.0,
                total=174.0,
                created_at=datetime(2023, 1, 2, 12, 0, 0),
                cancel_at=datetime(2023, 1, 3, 12, 0, 0)
            )
            db.session.add_all([order1, order2])
            db.session.commit()

        # Send a GET request to the orders/order endpoint with a cancel_at filter
        response = self.client.get('orders/order?cancel_at=2023-01-03T00:00:00')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json)
        self.assertEqual(len(response.json['orders']), 1)
        self.assertEqual(response.json['orders_qty'], 1)

    def test_get_all_orders_no_orders_found(self):
        # Send a GET request to the orders/order endpoint
        response = self.client.get('orders/order')

        # Verify the response
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'No orders found')

if __name__ == '__main__':
    unittest.main()
