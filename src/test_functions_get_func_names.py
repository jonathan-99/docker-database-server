import unittest
import functions

class Test_Get_Func_Names(unittest.TestCase):
    def test_get_func_names(self):
        os.chdir("C:/Users/local_admin/PycharmProjects/docker-database-server")
        output = functions.get_func_names('app.py')
        expected_return = ['/',
                   '/get-column/tablename-columnname',
                   '/get/all',
                   '/add_data/table_name/input_data',
                   '/create_table/table_name',
                   '/get-all-table]']
        with self.subTest():
            self.assertIsInstance(type(output), list)
        with self.subTest():
            self.assertEqual(output, expected_return)