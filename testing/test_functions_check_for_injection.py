import unittest
import os
import src.functions as functions


class Test(unittest.TestCase):
    def test_is_sql_injection_attack(self):
        os.chdir("//")
        with self.subTest('comment injection'):
            output = functions.is_injection_attack('--')
            self.assertTrue(output)
        with self.subTest('comment injection'):
            output = functions.is_injection_attack('SHOW *;')
            self.assertFalse(output)

if __name__ == '__main__':
    unittest.main()