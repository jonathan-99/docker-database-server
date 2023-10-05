import unittest
import src.app as application
import json
import requests
import src.sql_class as db
import os

class TestFunctionality(unittest.TestCase):
    def setUp(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        application.create_app(7000)
        database = db.DataBase('test')
        return_json = database.get_all()
        # add a check of return_json
        print("setup from test - {}".format(return_json))

    def test_main(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        def_url = 'http//127.0.0.1:7000/'
        with self.subTest('return index, so we know the app works'):
            r = requests.get(def_url + 'index.html')
            print("Return of request: ", r)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), r.text)
        with self.subTest('01 - end to end, get the table, add a value, get the table again'):
            r1 = requests.get(def_url + 'get-all-table')
            print("Return of request: ", r1)
            # add a return checker
            self.assertTrue(type(r1), json)
            r2 = requests.get(def_url + '/create-table/functional-test-01')
            print("Return of request: ", r2)
            # add a return checker
            self.assertTrue(type(r2), json)


if __name__ == '__main__':
    unittest.main()
