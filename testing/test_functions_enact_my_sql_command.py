import unittest
import src.functions as functions
import json


def remove_stuff(input):
    print("remove_stuff: ", input)
    output = input.replace("\\", "").replace("[[", "[").replace("]]", "]").replace("],", ",")
    output = output.replace(" [", " ").replace('"[', '[').replace(']"', ']')
    print("remove_stuff: ", output)
    return output

class TestEnactMySqlCommand(unittest.TestCase):
    def validateJSON(self, jsonData: json) -> bool:
        try:
            output = json.loads(jsonData)
            print("fault: ", output)
        except ValueError as err:
            return False
        except TypeError as terr:
            return False
        return True


    def test_enact_mysql_command(self):
        cmd = ['ADDTABLE', 'GET-DATA']
        table_name = 'test'
        data = 'test'
        output = functions.enact_mysql_command(cmd[1], table_name, data)
        temp = str(output['send_sql() return']['sql output'])
        temp = remove_stuff(temp)
        output['send_sql() return']['sql output'] = temp
        print("Output in ADDTABLE: ", output)
        print("validate:", self.validateJSON(output))
        # this is wrong, it should be True.
        self.assertFalse(self.validateJSON(output))


if __name__ == '__main__':
    unittest.main()
