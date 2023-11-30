import unittest
import json
from flask import Flask
from api import create_app, db


class OrdersTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()



#-----------------CREATE ORDERS-----------------
    def test_create_order(self):
        # Define a sample order payload
        order_payload = {
            "client_name": "John Doe",
            "articles": [
                {"article_name": "Product 1", "price": 10.0, "quantity": 2},
                {"article_name": "Product 2", "price": 15.0, "quantity": 1}
            ]
        }

        # Send a POST request to the orders/order endpoint
        response = self.client.post('orders/order', data=json.dumps(order_payload), content_type='application/json')

        # Verify the response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'Order created successfully')

    def test_create_order_invalid_payload(self):
        # Test with invalid payload
        invalid_payload = {"invalid_key": "invalid_value"}
        response = self.client.post('orders/order', data=json.dumps(invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Missing required fields')

if __name__ == '__main__':
    unittest.main()
