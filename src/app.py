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
except Exception as e:
    print("importing error: ", e)


app = Flask(__name__)


@app.route('/')
def index():
    """
    Default index page which will show database stats: size, last entry.
    :return:
    """
    return render_template('index.html')


@app.route("/create_table/<str:table_name>")
def api_create_table(table_name) -> json:
    """
    Simple api to get all data from database through functions.py
    :return:
    """
    safe = functions.check_input(table_name)
    if "QWERTY" in safe:
        outgoing = functions.get_all_data()
    else:
        outgoing = functions.create_table(safe)
    return outgoing


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
