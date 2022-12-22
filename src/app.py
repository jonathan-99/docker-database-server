#!/usr/bin/env python3

"""
This is the main python file running the flask app.
"""

try:
    import datetime
    import os
    import sys
    import time
    import logging
    from flask import Flask, render_template
    import functions
    import json
    import jinja2
except Exception as e:
    print("importing error: ", e)


app = Flask(__name__, template_folder='../templates')


@app.route('/')
def index():
    """
    Default index page which will show database stats: size, last entry.
    :return:
    """
    return render_template("index.html")


@app.route("/create_table/<string:table_name>")
def api_create_table(table_name) -> json:
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    safe = functions.check_input(table_name)
    db_exists = functions.check_table(safe)
    if ("QWERTY" in safe) and db_exists:
        outgoing = functions.get_all_data()
    else:
        outgoing = functions.create_table(safe)
    return outgoing

@app.route("/add_data/<string:input_data>")
def api_add_data(input_data) -> json:
    """
    This takes data from any source, containing any data, and adds it to a known table.
    requires input_data to be in the following format.
    device-id : ip address
    table-name : weather
    data (list): "20221209 23", 12.3
    :param (list) input_data:
    :return (json) output_data:
    """
    # check input first
    output_data = json.dumps(input_data)
    return functions.add_data(output_data)

@app.route("/get-all-data")
def api_get_all_data():
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    return functions.get_all_data()


if __name__ == '__main__':
    config = functions.get_config()
    total_path = config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())

    app.run(debug=True, port=7000)
