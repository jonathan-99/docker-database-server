import unittest
import src.sql_class as sql_class
import json

class TestErrorTranslation(unittest.TestCase):
    def test_error_translation(self):
        with self.subTest():
            output = sql_class.error_translation(int(0))
            self.assertEqual(output['Error'][3:], 'This is a new Error to MySQL')
        with self.subTest():
            output = sql_class.error_translation(int(1))
            self.assertEqual(output['Error'][3:], 'Global Error')
        with self.subTest():
            output = sql_class.error_translation(int(1050))
            self.assertEqual(output['Error'][7:], '1050. Table already exists')

if __name__ == '__main__':
    unittest.main()