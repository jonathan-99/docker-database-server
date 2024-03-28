import unittest
import requests
import json
import requests
import time
import multiprocessing

import src.app as app

class TestAddWeatherDataEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = multiprocessing.Process(target=app.run_app, args=(6005,))
        cls.process.start()
        time.sleep(10)  # Wait for the Flask app to start

    def test_add_weather_data(self):
        print(f'test_add_weather_data()')
        # Define the JSON data to send in the POST request
        data = {
            "metadata": {
                "version": 1.0,
                "date_submitted": "2024-03-13T12:00:00",
                "date_received": "2024-03-13T12:00:00",
                "filename": "2024-03-13.txt",
                "src_ip": "127.0.0.1",
                "hostname": "localhost"
            },
            "data": [
                {
                    "timestamp": "2024-03-13T12:00:00",
                    "speed": 0.5
                },
                {
                    "timestamp": "2024-03-13T12:15:00",
                    "speed": 0.6
                }
            ]
        }

        # Send a POST request to the Flask app
        try:
            response = requests.post('http://127.0.0.1:6005/add-weather-data', json=data)
        except EOFError as err:
            print(f'This is a send error - {err}')
        except ConnectionError as conn_err:
            print(f'ConnectionError - {conn_err}')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # You can add more assertions here if needed

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.join()

if __name__ == '__main__':
    unittest.main()
