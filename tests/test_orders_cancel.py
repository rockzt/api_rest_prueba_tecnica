import unittest
import json
from flask import Flask
from api import create_app, db
from api.orders import models
from datetime import datetime

class CancelOrderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_cancel_order(self):
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

        # Send a PUT request to the orders/order/<order_id>/cancel endpoint
        response = self.client.put('orders/order/1/cancel')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Order canceled successfully')

        # Check if the order's cancel_at timestamp has been updated
        with self.app.app_context():
            updated_order = models.Order.query.get(1)
            self.assertIsNotNone(updated_order.cancel_at)

    def test_cancel_order_invalid_id(self):
        # Send a PUT request to the orders/order/<order_id>/cancel endpoint with an invalid ID
        response = self.client.put('orders/order/0/cancel')

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Invalid order ID')

    def test_cancel_order_not_found(self):
        # Send a PUT request to the orders/order/<order_id>/cancel endpoint with a non-existing ID
        response = self.client.put('orders/order/999/cancel')

        # Verify the response
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Order not found')

    def test_cancel_order_already_canceled(self):
        # Create a sample canceled order in the database
        with self.app.app_context():
            order = models.Order(
                client_name='John Doe',
                subtotal=100.0,
                iva=16.0,
                total=116.0,
                created_at=datetime(2023, 1, 1, 12, 0, 0),
                cancel_at=datetime.now()
            )
            db.session.add(order)
            db.session.commit()

        # Send a PUT request to the orders/order/<order_id>/cancel endpoint for the already canceled order
        response = self.client.put('orders/order/1/cancel')

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Order is already canceled')


if __name__ == '__main__':
    unittest.main()
