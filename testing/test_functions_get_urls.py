import unittest
from src import functions
import os

class TestFunctionsGetURLS(unittest.TestCase):
    def test_get_func_names(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        output = functions.get_urls('src/app.py')
        expected = ['/create-table', '/add-data', '/get/', '/get-all', '/get-column']
        with self.subTest():
            self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()