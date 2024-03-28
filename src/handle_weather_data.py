#!/usr/bin/env python3

import json
import logging
from src.class_weather_data_model import WeatherConfigurationSchema as model
from src.class_weather_data_model import weather_data_model_manager as manager


# first check the src ip is the same as that in the model.

# add model data to sql database.
## need to create table format.

def manage_weather_data(input_json: json, input_src_ip: str) -> json:
    """
    This will accept the model json, validate it, then put it into the database.
    """
    returned_value = manager.find_src_ip_in_model(input_json, input_src_ip)
    if returned_value == input_src_ip:
        list_of_all_keys = manager.get_all_keys(input_json)
        list_of_keys_to_validate = manager.remove_validation_items(list_of_all_keys)
        for item in list_of_keys_to_validate:
            manager.validate_this(item, input_json, )
    else:
        print(f'sent information does not confirm to host ip - {returned_value} and {input_src_ip}')
        logging.warning(f' In manage_weather_datat(), sent information does not confirm to host ip - {returned_value} and {input_src_ip}')
    return_json = {'output': 'test'}
    return return_json

def refactor_incoming_json_into_weather_model(in_json: json):
    logging.debug(f'refactor_incoming_json_into_weather_model() - {in_json}')
    m = manager.__init__(in_json)

    # next is to add model to db.

if __name__ == '__main__':
    print(f'This is the handle_weather_data.py -')