#!/usr/bin/env python3

import json
import logging
import os
from marshmallow import Schema, fields

class WeatherConfigurationSchema(Schema):
    class Meta:
        fields = ("version", "date_submitted", "date_received", "filename", "src_ip", "hostname")

    version = fields.Float()
    date_submitted = fields.DateTime()
    date_received = fields.DateTime()
    filename = fields.String()
    src_ip = fields.String()
    hostname = fields.String()

    # Define the nested schema for the 'data' field
    class DataSchema(Schema):
        fields = ("datetime", "speed")

    datetime = fields.DateTime()
    speed = fields.Float()

    data = fields.Nested(DataSchema)

    relationship = fields.Dict()

    validation = fields.Dict()

class weather_data_model_manager():
    def __init__(self, input_json: json):
        # Load the JSON data using the schema
        schema_instance = WeatherConfigurationSchema().load(input_json)

        # Print the loaded data
        print(f'This is class weather_data_model_manager - {schema_instance}')

    def get_absolute_path(local_filename):
        # If the filename is provided without a path, assume it is in the 'data' directory
        if not os.path.isabs(local_filename):
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            logging.debug(f'data_dir - {data_dir}')
            data_dir = data_dir.replace('\\src', '')
            local_filename = os.path.join(data_dir, local_filename)
            logging.debug(f'local_filename - {local_filename}')
        return local_filename

    def print_pretty_json(input_data):
        try:
            # Convert the parsed data to JSON with indentation for better readability
            pretty_json = json.dumps(input_data, indent=2)
            print(f'Parsed Data - {pretty_json}')
        except Exception as e:
            logging.error(f"An error occurred while printing JSON data: {str(e)}")

    def find_src_ip_in_model(json_obj, target_key):
        """
        Recursively search for a target key in a JSON object.

        Args:
        - json_obj (dict): The JSON object to search.
        - target_key (str): The key to search for.

        Returns:
        - The value corresponding to the target key if found, None otherwise.
        """
        # Base case: If json_obj is not a dictionary, return None
        if not isinstance(json_obj, dict):
            return None

        # Check if the target key exists in the current level of the JSON object
        if target_key in json_obj:
            return json_obj[target_key]

        # Recursive case: Iterate through the values of the current level
        for value in json_obj.values():
            # Recursively search each value
            result = find_src_ip_in_model(value, target_key)
            if result is not None:
                return result

        # If the target key is not found at any level, return None
        return None

    # need to iterate through the model with each validate value and check it is valid.
    def get_all_keys(json_obj: json) -> list:
        """
        Recursively extract all keys from a JSON object.

        Args:
        - json_obj (dict): The JSON object to extract keys from.

        Returns:
        - A list containing all keys from the JSON object.
        """
        keys = []

        # Base case: If json_obj is not a dictionary, return an empty list
        if not isinstance(json_obj, dict):
            return keys

        # Iterate through the key-value pairs in the JSON object
        for key, value in json_obj.items():
            # Add the current key to the list of keys
            keys.append(key)
            # If the value is a nested dictionary, recursively extract keys from it
            if isinstance(value, dict):
                keys.extend(get_all_keys(value))
        return keys

    def append_suffix_to_list(input_list: list) -> list:
        output_list = [item + '_validation' for item in input_list]
        return output_list

    def remove_validation_items(in_list: list) -> list:
        """
        Remove items containing the word 'validation' from the given list and remove the underscore.
        Args:
        - lst (list): The list of items.
        Returns:
        - A new list with items containing 'validation' removed and underscores removed from those items.
        """
        return [item.replace('_', '') for item in in_list if 'validation' not in item]

    import re

    def validate_this(valid_key_name: str, json_object_to_search: json, value_to_validate: str) -> bool:
        # iterate through json giving key, values
        for key, value in json_object_to_search.item():
            # when key equals the key we are after, then compare the regex
            if key == valid_key_name:
                # Compile the regex pattern
                regex = re.compile(json_object_to_search[key])
                if regex.match(value):
                    return True
                else:
                    return False


    def iterate_json_list(json_object: json, key_to_match: list):
        for key in key_to_match:
            if key in json_object:
                appended_value = str(key) + '_validation'
                validate_this(appended_value, json_object, json_object[key])

