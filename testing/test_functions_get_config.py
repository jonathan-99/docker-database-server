import unittest
import src.functions as functions
import os


class TestGetConfig(unittest.TestCase):
    def test_get_config(self):
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        output = functions.get_config('src/config.json')
        with self.subTest():
            self.assertEqual(output.get_logging_path(), 'logging/')
        with self.subTest():
            self.assertEqual(output.get_log_filename(), 'debugger.log')
        with self.subTest():
            self.assertIsInstance(output.show_all(), str)


if __name__ == '__main__':
    unittest.main()
