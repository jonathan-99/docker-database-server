import unittest
import os
import json
import src.sql_class as sql_class


def _json_checker(input_value):
    """
    This is an internal checker within this class to check if something is in json format.
    """
    try:
        json.loads(input_value)
    except ValueError as e:
        print("e {}".format(e))
        return False
    return True


class TestDataBase(unittest.TestCase):

    def test_database_initiation(self):
        """
        This test the creation of a Database() object.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        with self.subTest('test_database_object_creation'):
            self.assertIsInstance(s, sql_class.DataBase)

    def test_get_database_name(self):
        """
        This tests the retrieval of a database name.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        return_test_get_database_name = s.get_database_name()
        with self.subTest('test_get_database_name returns something'):
            self.assertEqual(type(return_test_get_database_name), str)
        with self.subTest('test_get_database_name returns the test database name'):
            self.assertEqual(return_test_get_database_name, 'testing/database_name.db')

    def test__check_sql_statement(self):
        """
        This checks that the in-built sqlite3 method works
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        self.statement = "SHOW ALL;"
        self.bad_statement = "now"
        self.dodgy_statement = "--;"
        return_test__check_sql_statement = s._check_sql_statement(self.statement)
        return_test_bad = s._check_sql_statement(self.bad_statement)
        with self.subTest('check the check works!'):
            self.assertEqual(type(return_test__check_sql_statement), bool)
        with self.subTest('is it a correct return'):
            self.assertTrue(return_test__check_sql_statement)
        with self.subTest('check a bad statement'):
            self.assertFalse(return_test_bad)
        with self.subTest('check for dodgy-ness in sql statement'):
            self.assertTrue(False)

    def test_check_database_exists(self):
        """
        This checks both databases exists.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s_test = sql_class.DataBase('test')
        s_main = sql_class.DataBase('main')
        with self.subTest('positive database exists'):
            self.assertTrue(s_test.check_database_exists('testing/database_name.db'))
        with self.subTest('negative database exists'):
            self.assertFalse(s_test.check_database_exists('testing/stuff.db'))
        with self.subTest('check the main database exists'):
            self.assertTrue(s_main.check_database_exists('src/database_name.db'))

    def test_check_table_exists(self):
        """
        This checks to see if the table exists function works
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        object_test = sql_class.DataBase('test')
        with self.subTest('test check table exists - is there a return value'):
            self.assertEqual(type(object_test), bool)
        with self.subTest('test if table exists - correct return'):
            self.assertTrue(object_test)

    def test_add_table(self):
        """
        This tests if a table exists and create a table, and add values into a table.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        self.table_name_good = "test_table001"
        self.ip_add_good = '127.0.0.1'
        self.pi_name_good = ['pinas', 'weather']
        self.speed = 12.2
        self.time = "2023-08-22"
        with self.subTest('Test if test_table exists'):
            statement = "SELECT name FROM {} WHERE type='table' AND name='{}'".format('sqlite_master',
                                                                                      self.table_name_good)
            output = s._send_sql(s.get_database_name(), statement)
            self.assertEqual('[]', output['send_sql() return']['sql output'])
        with self.subTest('create a table'):
            sql_statement = "CREATE table {} VALUES ('{}', '{}')".format(self.table_name_good, 'speed INT', 'time TEXT')
            output = s._send_sql(s.get_database_name(), sql_statement)
            print("-- output -- {} -- {}".format(output, output['send_sql() return']['sql output']))
            self.assertEqual('[]', output['send_sql() return']['sql output'])
        with self.subTest('insert values into a table'):
            sql_statement = "INSERT INTO {} VALUES ('{}', '{}')".format(self.table_name_good, self.pi_name_good[0],
                                                                        self.pi_name_good[1])
            output = s._send_sql(s.get_database_name(), sql_statement)
            print("-- output -- {} -- {}".format(output, output['send_sql() return']['sql output']))
            self.assertEqual('[]', output['send_sql() return']['sql output'])

    def test_add_data_to_table(self):
        """
        This will test adding data to an existing table.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        self.input_data = ['one1', 'two2', 3]
        self.device_id = 'test_pinas'
        self.table_name = 'test_table_name'
        with self.subTest('Add data to a table'):
            self.assertTrue(s.add_data_to_table(self.device_id, self.table_name, self.input_data))

    def test_get_data_from_table(self):
        """
        This will test if the return is json format only.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        output_value = s.get_data_from_table('test', ['one1', 'two2'])
        with self.subTest('format returned is json'):
            format_value = _json_checker(output_value)
            self.assertTrue(format_value)
        with self.subTest('what comes back'):
            if '' in output_value['send_sql() return': 'sql output']:
                self.assertTrue(True)
            else:
                internal_error = "sql_class.add_table() error - {}".format(output_value)
                print(internal_error)
                self.assertTrue(False)

    def test_get_table_names(self):
        """
        Need to test if this will retrieve the table names.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        test_object = sql_class.DataBase('test')
        return_test_table_names = test_object.get_table_names()
        with self.subTest('test get table names returns something'):
            self.assertEqual(type(return_test_table_names), json)
        with self.subTest('test returns the correct tables names'):
            print("test_get_table_names() - {}".format(return_test_table_names))
            self.assertTrue(False)

    def test_get_column_names_from_table(self):
        """
        Testing to get the column names from a specific table.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        test_object = sql_class.DataBase('test')
        print("test_get_column_names_from_table() - {}".format(test_object.get_table_names()))
        # need to filter table names
        # this next line will error
        return_test_get_column_names = test_object.get_column_names_from_table(test_object.get_table_names())
        with self.subTest('test get column names from table - returns something'):
            self.assertEqual(type(return_test_get_column_names), json)
        with self.subTest('test get column names from table - are correct'):
            self.assertTrue(False)

    def test_get_table_details(self):
        """
        This will test if we get the column headers.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        output_value = s.get_table_details('test')
        with self.subTest('is it in json format'):
            format_value = _json_checker(output_value)
            self.assertTrue(format_value)

    def test_get_all(self):
        """
        This function will return all data in the table in a json format.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        output_value = s.get_table_details('test')
        with self.subTest('is it in json format'):
            format_value = _json_checker(output_value)
            self.assertTrue(format_value)

    def test_get_statistics(self):
        """
        This function gets all the metadata around the database in a json format.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        output_value = s.get_table_details('test')
        with self.subTest('is it in json format'):
            format_value = _json_checker(output_value)
            self.assertTrue(format_value)

    def test__send_sql(self):
        """
        This tests the connection and return of the private _send_sql function.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        test_object = sql_class.DataBase('test')
        return_send_sql = test_object.get_all()
        with self.subTest('Does it function and return data in json format'):
            self.assertEqual(type(return_send_sql), json)


if __name__ == '__main__':
    unittest.main()
