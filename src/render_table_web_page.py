#!/usr/bin/env python3

try:
    import datetime
    import os
    import sys
    import time
    import logging
    import json
    from src import functions
except Exception as e:
    print("importing error: ", e)

def html_table(input_value) -> list:
    """
    This function takes values and places them in a html list
    :param input_value:
    :return list:
    """
    logging.debug("html_table")

    output = ['<table>']
    for sublist in input_value:
        output.append('<tr><td>')
        output.append('{}</td><td>'.format(sublist))
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

def generate_html_page(name_of_page: str) -> None:
    """
    This gets a list of file names and creates a small html page with those names
    :return:
    """
    logging.basicConfig(filename='logging/log.txt')
    logging.debug('simple browser generate_html_page() with page ' + name_of_page)

    title, end_tags = create_html_page_wrapper('URL options')

    input_value = functions.get_directory_listing()
    table = html_table(input_value)

    table.insert(0, title)
    table.append(end_tags)

    filename = 'templates/{}.html'.format(name_of_page+'.html')
    characters_to_remove = [',', "'", "[", "]"]
    new_table = str(table)

    for x in range(0, len(characters_to_remove)):
        new_table = new_table.replace(characters_to_remove[x], "")

    if os.path.exists(filename):
        reply = "file {} exists, deleting it.".format(name_of_page)
        print(reply)
        os.remove(filename)
    else:
        pass
    try:
        with open('templates/' + name_of_page + ".html", "w") as fileObject:
            fileObject.write(new_table)
    except FileExistsError as e:
        print("<html><body><h1>" + "File Error" + "</h1></body></html>")
        logging.error("File Exists Error in generate_html_page()", exc_info=True)
    return