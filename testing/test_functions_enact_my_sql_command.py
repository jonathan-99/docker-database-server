import unittest
import src.functions as functions
import json


class TestEnactMySqlCommand(unittest.TestCase):
    def validateJSON(self, jsonData: json) -> bool:
        try:
            json.loads(jsonData)
        except ValueError as err:
            return False
        return True


    def test_enact_mysql_command(self):
        cmd = ['ADDTABLE', 'GET-DATA']
        table_name = 'test'
        data = 'test'
        output = functions.enact_mysql_command(cmd[1], table_name, data)
        with self.subTest():
            self.assertTrue(self.validateJSON(output))


if __name__ == '__main__':
    unittest.main()
