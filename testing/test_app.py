import unittest
import src.app as application
import os
import json
import requests


class TestApp(unittest.TestCase):
    global domain, return_value, status_code
    domain = 'http://127.0.0.1:6000'
    return_value = {"return": "value"}
    status_code = 200

    def setup_app(self, patch_create_table): #reference patch
        patch_create_table.return_value = self.response

    def test_create_app(self):
        """
        This testing the app is created.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        with self.subTest('creating a app'):
            port_num = 6000
            test_url = domain # '127.0.0.1:{}'.format(port_num)
            application.create_app(port_num)
            return_value = requests.request(test_url)
            self.assertEqual(return_value.status_code, status_code)

    def test_index(self):
        """
        This purely tests the function.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(6001)
        with self.subTest('Testing index'):
            return_value = application.index()
            print("{} - {}".format(self.__module__, return_value))


    def test_api_get_table_names(self):
        """
        This test the functionality of only getting all data.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(6002)
        with self.subTest('Get a json format answer'):
            return_value_01



if __name__ == '__main__':
    unittest.main()
