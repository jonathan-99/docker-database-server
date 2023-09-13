import unittest
import os
import src.functions as functions


class Test(unittest.TestCase):
    def test_get_directory_listing(self):
        os.chdir("//")
        with self.subTest('default'):
            output = functions.get_directory_listing()
            expected_output = ['create_app', 'index', 'api_create_table', 'api_add_data', 'api_get_data',\
                               'api_get_table_names', 'api_get_column_data']
            self.assertEqual(output, expected_output)
        with self.subTest('return is in a list type'):
            output = functions.get_directory_listing()
            self.assertEqual(type(output), list)

if __name__ == '__main__':
    unittest.main()