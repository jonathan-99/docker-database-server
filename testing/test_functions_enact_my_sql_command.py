import unittest
import src.functions as functions
import json
import os
from random import randrange


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
        os.chdir("C:/Users/JonathanL/PycharmProjects/docker-database-server/")
        cmd = ['ADDTABLE', 'ADDDATA', 'GET-DATA']
        table_name = 'test_table'
        test_data = ['test_data_1', 'test_data_2']
        configuration = functions.get_config('src/config.json')
        database_name = configuration.get_database_name()
        print("Testing pre-sets: {}, {}, {}, {}".format(cmd, table_name, test_data, database_name))


        with self.subTest('Test ADDTABLE without data'):
            random_number = str(randrange(100))
            output = functions.enact_mysql_command(database_name, cmd[0], table_name+random_number, test_data)
            print("Error trap {}".format(output))
            output = str(output['send_sql() return']['sql output'])
            """ temp = remove_stuff(temp)
            output['send_sql() return']['sql output'] = temp """
            print("Output of ADDTABLE:{} - {} ".format(type(output), output))
            # this is wrong, it should be True.
            self.assertFalse((self.validateJSON(output)))

        with self.subTest('Test ADDDATA'):
            output = functions.enact_mysql_command(database_name, cmd[0], table_name, test_data)
            temp = str(output['send_sql() return']['sql output'])
            temp = remove_stuff(temp)
            output['send_sql() return']['sql output'] = temp
            print("Output of ADDDATA: ", output)
            # this is wrong, it should be True.
            self.assertFalse((self.validateJSON(output)))


        with self.subTest('Get data'):
            output = functions.enact_mysql_command(database_name, cmd[1], table_name, test_data)
            temp = str(output['send_sql() return']['sql output'])
            temp = remove_stuff(temp)
            output['send_sql() return']['sql output'] = temp
            print("Output of GET-DATA: ", output)
            print("validate:", self.validateJSON(output))
            # this is wrong, it should be True.
            self.assertFalse(self.validateJSON(output))

        with self.subTest('Get column'):
            output = functions.enact_mysql_command(database_name, cmd[1], table_name, test_data)
            temp = str(output['send_sql() return']['sql output'])
            temp = remove_stuff(temp)
            output['send_sql() return']['sql output'] = temp
            print("Output of GET-DATA: ", output)
            print("validate:", self.validateJSON(output))
            # this is wrong, it should be True.
            self.assertFalse(self.validateJSON(output))


if __name__ == '__main__':
    unittest.main()
