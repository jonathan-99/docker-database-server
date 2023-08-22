import unittest
import os
import src.functions as functions


class Test(unittest.TestCase):
    def test_html_table(self):
        validation_service = 'http://validator.w3.org/'
        os.chdir("//")
        good_list = ['a', 'b', 'c']
        with self.subTest('input list -> output list'):
            output = functions.html_table(good_list)
            self.assertEqual(type(output), list)


if __name__ == '__main__':
    unittest.main()

