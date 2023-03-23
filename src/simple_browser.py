#!/usr/bin/env python3

"""To set up a simple HTTP browser for seeing what has been logged."""

try:
    import sys
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from src import functions
    from src import render_table_web_page as render_table
    import logging
    import os
except ImportError as e:
    sys.exit("Importing error: " + str(e))

class WebServer(BaseHTTPRequestHandler):
    """
    This is a basic server class for serving a html file.
    """
    logging.debug("Within WebServer Class")
    os.chdir("C:/Users/local_admin/PycharmProjects/docker-database-server")

    def serve_page(self, page: str):
        self.path = 'templates' + page
        print("path: ", self.path)
        try:
            file_to_open = open(self.path).read()
            self.send_response(200)
        except FileNotFoundError as err:
            file_to_open = str(err)
            self.send_response(404)
            logging.error("File Not Found Error - in serve_page()", exc_info=True)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))

    def do_GET(self) -> bool:
        if self.path == "/":
            self.serve_page("/index.html")
            logging.debug("Served main index.html page")
            return True
        else:
            self.serve_page("/index.html")
            self.send_response(303, "this is not where you want to be.")
            logging.debug("Served table.html page.")
            return False


def setup() -> None:
    # set up pre-pages
    if os.path.exists('template/table.html'):
        pass
    else:
        render_table.generate_html_page("table")

    # plot of newest data
    server = HTTPServer(('localhost', 7000), WebServer)
    status = "Serving on: " + str(server.server_name) \
        + " addr: " \
        + str(server.server_address) \
        + " port: " \
        + str(server.server_port)
    print(status)
    logging.debug(status)
    server.serve_forever()


if __name__ == '__main__':
    logging.basicConfig(filename='logging/log.txt')
    setup()