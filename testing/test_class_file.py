import unittest
import src.class_file as class_file
import os

class TestConfigData(unittest.TestCase):

    @classmethod
    def test_create_instance(self):
        """
        Can it create an instance?
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        self.assertIsInstance(self, obj=configuration, cls=class_file.ConfigData)



    def test_database_name(self):
        """
        There is an assumption here that if setting and getting database_name works, test_database_name works too.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_database_name(self)'):
            expected_name = 'src/database_name.db'
            output_result = configuration.get_database_name()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set_database_name(self)'):
            input_name = 'testing/database_name.db'
            configuration.set_database_name(input_name)
            output_result = configuration.get_database_name()
            self.assertEqual(input_name, output_result)



    def test_setting_path(self):
        """
        This tests the setting and getting of path config.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_path_name(self)'):
            expected_name = '/opt/docker-database-server/'
            output_result = configuration.get_path()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set_path_name(self)'):
            input_name = '/test/docker-database-server/'
            configuration.set_path(input_name)
            output_result = configuration.get_path()
            self.assertEqual(input_name, output_result)

    def test_logging_path(self):
        """
        This tests the setting and getting of the logging path.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_logging_path(self)'):
            expected_name = "logging/"
            output_result = configuration.get_logging_path()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set__logging_path(self)'):
            input_name = '/test/logging_path/'
            configuration.set_logging_path(input_name)
            output_result = configuration.get_logging_path()
            self.assertEqual(input_name, output_result)

    def test_log_filename(self):
        """
        This will test the getting and setting of log_filename.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_log_filename(self)'):
            expected_name = "debugger.log"
            output_result = configuration.get_log_filename()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set_log_filename(self)'):
            input_name = '/test/test_log.log'
            configuration.set_log_filename(input_name)
            output_result = configuration.get_log_filename()
            self.assertEqual(input_name, output_result)

    def test_data_location(self):
        """
        This tests the getting and setting of the data location
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_data_location(self)'):
            expected_name = "data/"
            output_result = configuration.get_data_location()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set_data_location(self)'):
            input_name = '/test/data/'
            configuration.set_data_location(input_name)
            output_result = configuration.get_data_location()
            self.assertEqual(input_name, output_result)

    def test_server_port(self):
        """
        This tests the getting and setting of the server port.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_server_port(self)'):
            expected_name = 7000
            output_result = configuration.get_server_port()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set_server_port(self)'):
            input_name = 7001
            configuration.set_server_port(input_name)
            output_result = configuration.get_server_port()
            self.assertEqual(input_name, output_result)

    def test_logging_level(self):
        """
        This tests the getting and setting of the logging level.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('get_logging_level(self)'):
            expected_name = "logging.DEBUG"
            output_result = configuration.get_logging_level()
            self.assertEqual(expected_name, output_result)
        with self.subTest('set_logging_level(self)'):
            input_name = "logging.INFO"
            configuration.set_logging_level(input_name)
            output_result = configuration.get_logging_level()
            self.assertEqual(input_name, output_result)


    def test_show_all(self):
        """
        This tests the show_all function works.
        """
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        configuration = class_file.ConfigData()
        with self.subTest('show_all(self)'):
            expected_name = {'path': '/opt/docker-database-server/',
                             'logging_path': 'logging/',
                             'log_filename': 'debugger.log',
                             'src': 'src',
                             'data': 'data/',
                             'simple-server-port': 7000,
                             'logging-level': 'logging.DEBUG',
                             'database-name': 'src/database_name.db',
                             'test-database-name': 'testing/database_name.db'}
            output_result = configuration.show_all()
            self.assertEqual(expected_name, output_result)


if __name__ == '__main__':
    unittest.main()