import unittest
from unittest import mock
from mock import patch
import src.app as application
import flask
from flask import g
import json


class TestApp(unittest.TestCase):
    global domain, return_value, status_code
    domain = 'http://127.0.0.1:6000'
    return_value = {"return": "value"}
    status_code = 200
    global exceptional
    # B = A.api_add_table('test_a')
    # print("api_add_table in test: ", B)
    # def setUp(self, client):
    #     # Perform set up before each test, using client
    #     pass
    #
    # def tearDown(self, client):
    #     # Perform tear down after each test, using client
    #     pass


    def create_app(self):
        app = flask.Flask(__name__, template_folder='../templates')
        app.run(debug=True, host='127.0.0.1', port=6000)
        # self.exceptional = flask.flask_exceptional(self.app)
        return app

    @patch('src.app.index')
    def test_index(self, api):
        """
        Test \
        test \index.html
        test \index.html\
        test wrong input returns \index.html
        :param client:
        """
        m = mock.MagicMock()
        print("m: ", m.return_value)
        app = self.create_app()
        with self.subTest():
            """
            One version
            """

            with app.app_context() as c:
                output = c.app.post('/')
                print("output: ", output)
                return_value = output
                print("Serving index(): ", type(return_value), return_value)
                self.assertEqual(return_value.status_code, 200)
                self.assertIn("<br>", return_value)
                self.assertIsInstance(return_value, str)
                api.assertTrue(True)
        with self.subTest():
            """
            This one is using function example
            """
            # Create a test client using the Flask application configured for testing
            with app.test_client() as test_client:
                response = test_client.post('/')
                print("Response: ", response.status_code, " - ", response, " - ", app.route)
                self.assertEqual(response.status_code, 404)
        with self.subTest():
            """
            This one is using function example
            """
            # Create a test client using the Flask application configured for testing
            with app.test_client() as test_client:
                response = test_client.get('index.html')
                print("Response: ", response.status_code, " - ", response, " - ", app.route)
                self.assertEqual(response.status_code, 404)
    def test_api_create_table(self):
        """
        test add 'test_a_table'
        test add another 'test_a_table'
        :return:
        """
        pass


    def test_api_add_data(self):
        """
        test add to table test1: column_1, column_2
        test add to new table test2: column_1, column_2
        :return:
        """
        pass


    def test_api_get_data(self):
        """
        test get all tables (names) - subTest of api
        test get all column (data) information from tables - subTest of api
        test get all data from columns within tables
        :return:
        """
        pass


if __name__ == '__main__':
    unittest.main()
