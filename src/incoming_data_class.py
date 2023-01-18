#!/usr/bin/env python3

class Input_Format:
    """
    A simple way of creating flexible table entry for any device.
    """
    def __init__(self):
        self.device_id = ""
        self.table_name = []
        self.key_value = []

    def add(self, name: str, type_of_data: str) -> bool:
        if type_of_data == "dev":
            self.device_id = name
        elif type_of_data == "tab":
            self.table_name.append(name)
        elif type_of_data == "d":
            self.key_value.append(name)
        else:
            return False
        return True
