import unittest
import os
import sql_class

class TestDataBase(unittest.TestCase):
    def test_db_exists(self):
        """
        Test if db exists
        """
        os.chdir("//")
        table_name = 'test_table'
        data = ['pinas', 'weather', "127.0.0.1"]
        database_name = 'testing/database_name.db'
        output = os.path.isfile(database_name)
        self.assertTrue(output)

    def test_table_exists(self):
        """
        Tests if the table exists
        """
        os.chdir("//")
        table_name = 'test_table'
        data = ['pinas', 'weather', "127.0.0.1"]
        database_name = 'testing/database_name.db'
        db = sql_class.DataBase()
        #print("Testing pre-sets: {}, {}, {}, {}".format(table_name, data, database_name))
        with self.subTest('Test if test_table exists'):
            statement = "SELECT name FROM {} WHERE type='table' AND name='{}'".format('sqlite_master', table_name)
            output = db.send_sql(database_name, statement)
            self.assertEqual('[]', output['send_sql() return']['sql output'])

    def test_create_and_insert(self):
        """
        Tests inserting data after creating table
        """
        os.chdir("//")
        table_name = 'test_table'
        data = ['pinas', 'weather', r'127.0.0.1']
        database_name = 'testing/database_name.db'
        db = sql_class.DataBase()
        with self.subTest('Insert and show all'):
            """
            statement_create = "CREATE TABLE {} (host TEXT, data_type TEXT, ip_add TEXT)".format(table_name)
            output_1 = db.send_sql(database_name, statement_create)
            """
            statement_insert = "INSERT INTO {} VALUES ('{}', '{}', '{}')".format(table_name, data[0], data[1], data[2])
            output_2 = db.send_sql(database_name, statement_insert)
            print("Third test: ", output_2, output_2)
            self.assertEqual('[]', output_2['send_sql() return']['sql output'])
            statement_final = "SELECT * FROM {}".format(table_name)
            output_3 = db.send_sql(database_name, statement_final)
            print("Connection test: {}".format(output_3))
            self.assertNotEquals('[]', output_3['send_sql() return']['sql output'])
