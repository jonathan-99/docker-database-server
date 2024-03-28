import unittest
import src.app as application
import json

class TestFunctionalAppProcessJSON(unittest.TestCase):
    def test_process_json(self):
        test_data = {
            "metadata": {
                "version": 1.0,
                "date_submitted": "2024-03-13T12:00:00",
                "date_received": "2024-03-13T12:00:00",
                "filename": "2024-03-13.txt",
                "src_ip": "127.0.0.1",
                "hostname": "localhost"
            },
            "data": [
                {
                    "timestamp": "2024-03-13T12:00:00",
                    "speed": 0.5
                },
                {
                    "timestamp": "2024-03-13T12:15:00",
                    "speed": 0.6
                }
            ]
        }
        output_json = application.process_json(test_data)
        print(f'test_process_json - {output_json}')
        check_value = 'specific message'
        self.assertEqual(output_json[check_value], 'Received correct JSON data')


if __name__ == '__main__':
    unittest.main()
