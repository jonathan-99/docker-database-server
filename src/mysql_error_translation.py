#!/usr/bin/env python3

try:
    import os
    import sys
    import csv
    import json
    import logging
except ImportError as e:
    sys.exit("Importing error: " + str(e))


def error_translation(code) -> json:
    first = 'Error'
    second = ''
    if (code > 0) and (code < 1000):
        second = 'Global Error'
    elif (code > 999) and (code < 2000):
        if code == 1050:
            second += ' 1050. Table already exists'
        elif code == 1064:
            second += ' 1064. SQL syntax error?'
        elif code == 1146:
            second += ' 1146. Table does not seem to exist.'
        else:
            second = "Server error codes reserved for messages sent to clients."
    elif (code > 1999) and (code < 3000):
        if code == 2003:
            second += ' 2003. Can not connect to server - is it on?'
        else:
            second = "2000-2999. Client error codes reserved for use by the client library."
    elif (code > 2999) and (code < 4000):
        second = "3000-3999. Client error codes reserved for use by the client library."
    elif (code > 3999) and (code < 5000):
        second = "Server error codes reserved for messages sent to clients."
    elif (code > 4999) and (code < 6000):
        second = "Error codes reserved for use by X Plugin for messages sent to clients."
    elif (code > 9999) and (code < 50000):
        if code == 10061:
            second += ' 10061. Is your SQL database up? It cannot connect.'
        else:
            second = "Server error codes reserved for messages to be written to the error log (not sent to clients)."
    elif (code > 49999) and (code < 52000):
        second = "50,000 to 51,999: Error codes reserved for use by third parties."
    else:
        second = "This is a new Error to MySQL"

    if code == ER_ACCESS_DENIED_ERROR:
        second = "Something is wrong with your user name or password"
    elif code == ER_BAD_DB_ERROR:
        second = "Database does not exist"

    second = str(code) + ". " + second
    output = {first: second}
    logging.error("MySQL error." + str(output))
    return output
