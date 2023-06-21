from unittest.mock import MagicMock, patch
import unittest
import src.app as application
import json
import requests


class TestApp(unittest.TestCase):
    global domain, return_value, status_code
    domain = 'http://127.0.0.1:6000'
    return_value = {"return": "value"}
    status_code = 200

    def setUp(self) -> None:
        self.response = MagicMock('functions.enact_mysql_command', autospec=True)


    def setup_mock(self, patch_create_table): #reference patch
        patch_create_table.return_value = self.response

    @patch('src.app.api_create_table')
    def test_enact_mysql_command(self, mock_sql):
        good_table_name = "'ADDTABLE', test_1, ''"
        self.setup_mock("/create-table/test_1")  # patch_create_table=
        create_table_output = application.api_create_table(good_table_name)
        print("Return mock", return_value)
        print("mock_sql", create_table_output)
        self.assertEqual(return_value, create_table_output)
        self.assertIsInstance(mock_sql, MagicMock)

if __name__ == '__main__':
    unittest.main()
