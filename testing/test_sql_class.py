import unittest
import os
import src.sql_class as sql_class


class TestDataBase(unittest.TestCase):
    def test__check_sql_statement(self):
        os.chdir("//")
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
        os.chdir("//")
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
        os.chdir("//")
        s = sql_class.DataBase('test')
        with self.subTest('positive database exists'):
            self.assertTrue(s.check_database_exists('testing/database_name.db'))
        with self.subTest('negative database exists'):
            self.assertFalse(s.check_database_exists('testing/stuff.db'))
    def test_check_table_exists(self):
        self.fail()

    def test_add_table(self):
        os.chdir("//")
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
        self.fail()

    def test_get_data_from_table(self):
        self.fail()

    def test_get_table_details(self):
        self.fail()

    def test_get_all(self):
        self.fail()

    def test_get_statistics(self):
        self.fail()

    def test__send_sql(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()