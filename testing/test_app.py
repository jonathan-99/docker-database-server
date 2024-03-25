import unittest
import src.app as application
import os
import json
import requests


class TestApp(unittest.TestCase):
    domain = 'http://127.0.0.1:6000'
    return_value = {"return": "value"}
    good_status_code = 200
    port_number = 6000

    def test_create_app(self):
        """
        This testing the app is created.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        test_url = str(self.domain)  # '127.0.0.1:{}'.format(port_num)
        application.create_app(self.port_number)
        return_value_create_app = requests.request(method="POST", url=test_url)
        with self.subTest('test_creating_app return something'):
            self.assertEqual(return_value_create_app.status_code, self.good_status_code)
        with self.subTest('test_creating_app check contents'):
            self.assertTrue(False)

    def test_index(self):
        """
        This purely tests the function.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(self.port_number + 1)
        with self.subTest('Testing index'):
            return_value_index = application.index()
            print("{} - {}".format(self.__module__, return_value_index))

    def test_create_table(self):
        """
        This tests creation of a table only.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(self.port_number + 2)
        self.test_table_name = 'test' + str(self.port_number + 2)
        return_value_create_table = application.api_create_table()
        with self.subTest('Test to see if it comes back as a json'):
            self.assertEqual(type(return_value_create_table), json)
        with self.subTest('Test the contents of the return'):
            self.assertTrue(False)

    def test_api_add_data(self):
        """
        This tests the ability to add data to table.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(self.port_number + 3)
        self.test_table_name = 'test_api_add_data'
        self.device_id = "test_weather"
        self.input_data_simple_string = 'test_string'
        self.input_data_list = '12.3, 2023-08-22 01, 2.8, 2023-08-22 02'
        return_value_api_add_data = application.api_add_data(
            self.device_id,
            self.test_table_name,
            self.input_data_simple_string
        )
        with self.subTest('Json format'):
            self.assertEqual(type(return_value_api_add_data), json)
        with self.subTest('api_add_data() contents check'):
            self.assertTrue(False)
        with self.subTest('api_add_data() input validation'):
            self.assertTrue(False)

    def test_api_get_column_headers(self):
        """
        This is a test for getting column headers.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(self.port_number + 4)
        self.test_table_name = 'test_api_add_data'
        return_value_api_get_column_headers = application.api_get_column_headers()
        with self.subTest('api_get_column_headers is json format'):
            self.assertEqual(type(return_value_api_get_column_headers), json)
        with self.subTest('api_get_column_headers check return'):
            self.assertTrue(False)

    def test_api_get_data(self):
        """
        This tests the functionality of get specific data.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(self.port_number + 5)
        self.test_table_name = 'test'
        self.test_column_name = 'weather'
        return_value_api_get_data = application.api_get_data(self.test_table_name, self.test_column_name)
        print("api_get_data({},{})".format(self.test_table_name, self.test_column_name))
        print("api_get_data() -> {}".format(return_value_api_get_data))
        with self.subTest('Get a json format answer'):
            self.assertEqual(type(return_value_api_get_data), json)
        with self.subTest('Test the contents of the return'):
            self.assertTrue(False)

    def test_api_get_table_names(self):
        """
        This test the functionality of only getting all data.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(self.port_number + 6)
        return_value_api_get_table_names = application.api_get_table_names()
        print("Get table names: {}".format(return_value_api_get_table_names))
        with self.subTest('Get a json format answer'):
            self.assertEqual(type(return_value_api_get_table_names), json)
        with self.subTest('Test the contents of the return'):
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
