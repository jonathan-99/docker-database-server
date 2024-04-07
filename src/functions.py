#!/usr/bin/env python3

"""
The main functionality is referenced here.
"""

try:
    import datetime
    import re
    import os
    import sys
    import time
    import logging
    import json
    from src.class_file import ConfigData
    from src.sql_class import DataBase
    from src.injection_class import InjectorCheck
    import src.app as app
    from flask import jsonify
    from bs4 import BeautifulSoup
except Exception as e:
    print("importing error: ", e)

def is_injection_attack(input_statement: str) -> bool:
    """
    This will check if the inputted value has an injection attack in it, through the injector class object.
    """
    comment = '--'
    if comment in input_statement:
        return True
    else:
        return False


def append_to_div_in_html(html_file_path: str, appended_string: str) -> None:
    """
        A function that will open a html file called, index.html, search through until it finds a div tag with
        id='embedded-table-html' and then append a string inbetween that div.
    """

    def append_to_div_in_html(html_file_path, appended_string) -> None:
        logging.debug(f'append_to_div_in_html() - {html_file_path} - {appended_string}')
        try:
            # Open the HTML file
            with open(html_file_path, 'r') as file:
                html_content = file.read()

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the div tag with id="embedded-table-html"
            div_tag = soup.find('div', id='embedded-table-html')

            # Remove any existing content inside the div tag
            if div_tag:
                div_tag.clear()

            # Append the string inside the div tag
            if div_tag:
                div_tag.append(appended_string)

            # Write the modified HTML content back to the file
            with open(html_file_path, 'w') as file:
                file.write(str(soup))

            # check it worked
            with open(html_file_path, 'r') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            print(f"Appended successfully. {soup}")
        except Exception as e:
            print("An error occurred:", e)


def get_urls(filename: str) -> list:
    """
    This function traverses a file for any urls so that later it can be displayed to the user as possible options to use.
    :param filename:
    :return:
    """
    infile = open(filename)
    data = infile.readlines()
    result = []
    for line in data:
        matching = re.search(r'(@app\.route\(\")((/[a-z]*[-/][a-z]*))', line)
        if matching is not None:
            result.append(matching.group(2))
    infile.close()
    return result


def get_func_names(filename):
    """

    :param filename:
    :return:
    """
    infile = open(filename)
    data = infile.readlines()
    result = []
    for line in data:
        matching = re.search(r'\s*def (\w+)', line)
        if matching is not None:
            result.append(matching.group(1))
    infile.close()
    return result


def get_directory_listing(input_directory='testing/') -> list:
    names = get_func_names('src/app.py')
    urls = get_urls('src/app.py')
    input_list = ['/',
                  '/get-column/tablename-columnname',
                  '/get/all',
                  '/add_data/table_name/input_data',
                  '/create_table/table_name',
                  '/get-all-table]']
    return urls


def html_table(input_value: list) -> list:
    """
    This function takes values and places them in a html list
    :param input_value:
    :return list:
    """
    logging.debug("html_table")

    output = ['<table>']
    for sublist in input_value:
        output.append('<tr><td>')
        output.append('</td><td>'.join(sublist))
        output.append('</td></tr>')
    output.append('</table>')
    return output


def create_html_page_wrapper(name: str) -> tuple:
    """
    Need the start and end of a html page.
    :return: str, str
    """
    logging.debug("create_html_page_wrapper with " + name)

    title = "<!DOCTYPE html><head><title>" + name
    title += "</title></head><body>"
    end_tags = "</body></html>"
    return title, end_tags
