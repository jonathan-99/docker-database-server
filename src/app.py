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
    import flask
    from flask import Flask, jsonify
    from flask import render_template
    import functions
    import json
    import jinja2
    from flask_cors import CORS, cross_origin
except Exception as e:
    print("importing error: ", e)


app = flask.Flask(__name__, template_folder='../templates')
CORS(app)

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
    logging.debug('api_create_table')

    output = functions.enact_mysql_command('ADDTABLE', table_name)
    print("api_create_table: ", output)
    return jsonify(output)


@app.route("/add_data/<string:input_data>")
def api_add_data(input_data) -> json:
    """
    This takes data from any source, containing any data, and adds it to a known table.
    requires input_data to be in the following format.
    device-id : ip address
    table-name : weather
    data (list): "20221209 23", 12.3
    :param (str) input_data:
    :return (json) output_data:
    """
    output = functions.enact_mysql_command('ADDDATA', input_data)
    print("api_add_data: ", output)
    return jsonify(output)


@app.route("/get-all-data")
def api_get_all_data():
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    output = functions.enact_mysql_command('GET-ALL', 'THIS IS NOTHING')
    print("api_get_all_data: ", output)
    return jsonify(output)


if __name__ == '__main__':
    config = functions.get_config()
    total_path = config.get_logging_path() + config.get_log_filename()
    logging.basicConfig(filename=total_path, level=config.get_logging_level())

    app.run(debug=True, host='127.0.0.1', port=7000)
