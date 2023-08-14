import unittest
from src import functions
import os

class Test_Get_Func_Names(unittest.TestCase):
    def test_get_func_names(self):
        # os.chdir("C:\\Users\\local_admin\\PycharmProjects\\docker-database-server\\")
        os.chdir("C:\\Users\\JonathanL\\PycharmProjects\\docker-database-server\\")
        output = functions.get_func_names('src/app.py')
        expected_return_functions = ['index',
                                     'api_create_table',
                                     'api_add_data',
                                     'api_get_data',
                                     'api_get_table_names',
                                     'api_get_column_data']
        expected_return_url = ['index',
                   '/get-column/tablename-columnname',
                   '/get/all',
                   '/add_data/table_name/input_data',
                   '/create_table/table_name',
                   '/get-all-table]']
        with self.subTest():
            self.assertIs(type(output), list)
        with self.subTest():
            self.assertEqual(output[1], expected_return_functions[0])

if __name__ == '__main__':
    unittest.main()