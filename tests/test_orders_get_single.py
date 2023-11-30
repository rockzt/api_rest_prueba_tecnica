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

    def test_get_single_order(self):
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

        # Send a GET request to the orders/order/<order_id> endpoint
        response = self.client.get('orders/order/1')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.json)

    def test_get_single_order_invalid_id(self):
        # Send a GET request to the orders/order/<order_id> endpoint with an invalid ID
        response = self.client.get('orders/order/0')

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Invalid order ID')

    def test_get_single_order_not_found(self):
        # Send a GET request to the orders/order/<order_id> endpoint with a non-existing ID
        response = self.client.get('orders/order/999')

        # Verify the response
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Order not found')

if __name__ == '__main__':
    unittest.main()
