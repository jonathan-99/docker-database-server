import unittest
import json
from unittest.mock import patch
from flask import Flask
from src.app_routes import process_json
from src.handle_weather_data import manage_weather_data


class TestProcessJson(unittest.TestCase):

    def setUp(self):
        """ Set up a Flask test client and sample trace ID """
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.testing = True
        self.traceID = "test-trace-123"

    def create_http_call(self, key, value):
        """ Create an HTTP POST request with a JSON key-value pair """
        url = '/add-weather-data'  # The route you want to hit with the request
        data = {key: value}  # JSON data with the key-value pair
        return url, data

    def simulate_post_request(self, url, data):
        response = self.client.post(url, json=data)
        return response

    def orchestrate_post_requests(self):
        """ Orchestrates the process of testing both valid and invalid JSON post requests """

        # 1. Create valid JSON data (key-value pair)
        valid_data = self.create_http_call('key', 'value')

        # 2. Simulate POST request with valid data
        valid_response = self.simulate_post_request(valid_data)

        # Assert valid response status code and headers
        self.assertEqual(valid_response.status_code, 200)
        self.assertIn('X-Trace-Id', valid_response.headers)

        # 3. Create invalid JSON data (with None or invalid structure)
        invalid_data = self.create_http_call('key', None)  # Or use invalid data, like an empty string

        # 4. Simulate POST request with invalid data
        invalid_response = self.simulate_post_request(invalid_data)

        # Assert invalid response status code and headers
        self.assertEqual(invalid_response.status_code, 400)  # Assuming 400 for bad request
        self.assertNotIn('X-Trace-Id', invalid_response.headers)  # Assum


if __name__ == "__main__":
    unittest.main()
