import unittest
import os
import json
import src.sql_class as sql_class


class TestDataBase(unittest.TestCase):

    def _json_checker(self, input_value):
        try:
            json.loads(input_value)
        except ValueError as e:
            return False
        return True

    def test__check_sql_statement(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        with self.subTest('Good sql statement'):
            input_sql = "SHOW *;"
            output = s._check_sql_statement(input_sql)
            self.assertTrue(output)
        with self.subTest('Bad sql statement'):
            input_sql = "now"
            output = s._check_sql_statement(input_sql)
            self.assertFalse(output)

    def test__mysql_database_connection_details__(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        with self.subTest('testing database connection host details'):
            self.assertEqual(s._connection_host, '127.0.0.1')
        with self.subTest('testing database connection user details'):
            self.assertEqual(s._connection_user, 'user')
        with self.subTest('testing database connection password details'):
            self.assertEqual(s._connection_password, 'password')
        with self.subTest('testing database connection host details'):
            self.assertEqual(s._connection_port, 3306)

    def test_check_database_exists(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        with self.subTest('positive database exists'):
            self.assertTrue(s.check_database_exists('testing/database_name.db'))
        with self.subTest('negative database exists'):
            self.assertFalse(s.check_database_exists('testing/stuff.db'))
    def test_check_table_exists(self):
        self.fail()

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
            statement = "SELECT name FROM {} WHERE type='table' AND name='{}'".format('sqlite_master',\
                                                                                      self.table_name_good)
            output = s._send_sql(s.get_database_name(), statement)
            self.assertEqual('[]', output['send_sql() return']['sql output'])
        with self.subTest('create a table'):
            sql_statement = "CREATE table {} VALUES ('{}', '{}')".format(self.table_name_good, 'speed INT', 'time TEXT')
            output = s._send_sql(s.get_database_name(), sql_statement)
            print("-- output -- {} -- {}".format(output, output['send_sql() return']['sql output']))
            self.assertEqual('[]', output['send_sql() return']['sql output'])
        with self.subTest('insert values into a table'):
            sql_statement = "INSERT INTO {} VALUES ('{}', '{}')".format(self.table_name_good, self.pi_name_good[0],\
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
        input_data = ['one1', 'two2', 3]
        with self.subTest('Add data to a table'):
            self.assertTrue(s.add_data_to_table('test', input_data))

    def test_get_data_from_table(self):
        """
        This will test if the return is json format only.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        output_value = s.get_data_from_table('test', ['one1', 'two2'])
        with self.subTest('format returned is json'):
            format_value = self._json_checker(output_value)
            self.assertTrue(format_value)
        with self.subTest('what comes back'):
            if '' in output_value['send_sql() return': 'sql output']:
                self.assertTrue(True)
            else:
                internal_error = "sql_class.add_table() error - {}".format(output_value)
                print(internal_error)
                self.assertTrue(False)

    def test_get_table_details(self):
        """
        This will test if we get the column headers.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        s = sql_class.DataBase('test')
        output_value = s.get_table_details('test')
        with self.subTest('is it in json format'):
            format_value = self._json_checker(output_value)
            self.assertTrue(format_value)

    def test_get_all(self):
        self.fail()

    def test_get_statistics(self):
        self.fail()

    def test__send_sql(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()