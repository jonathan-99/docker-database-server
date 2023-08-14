from unittest.mock import MagicMock, patch
import unittest
import src.app as application
import json
import requests
import src.sql_class as db

class test_functionality(unittest.TestCase):
    def setUp(self):
        application.create_app()
        database = db.DataBase()
        return_json = database.send_sql("SHOW ALL")

    def test_main(self):
        r = requests.get('http://127.0.0.1:7000/index.html')
        print("Return of request: ", r)
        with self.subTest():
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), r.text)


if __name__ == '__main__':
    unittest.main()
