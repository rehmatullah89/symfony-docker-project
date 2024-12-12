#! /usr/bin/env python3

# Adapted from: https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7?permalink_comment_id=4241869#gistcomment-4241869

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys
import json
from typing import TypedDict

class ContactDto(TypedDict):
    phone_number: str


COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"
ALLOWED_PATHS = ['/send', '/bulk']

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def get_post_data(self):
        content_length = self.headers['Content-Length']
        content_length = 0 if (content_length is None) else int(content_length)
        post_data = self.rfile.read(content_length)
        return post_data


    def do_log(self, method):
        post_data = self.get_post_data()
        logging.info(COLOR + method + " request,\n" + RESET_COLOR + "Path: %s\nHeaders:\n%sBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write((method + " request for {}\n".format(self.path)).encode('utf-8'))


    def validate_contact(self, contact):
        try:
            if not contact['phone_number']:
                raise KeyError('phone_number')

            return ContactDto(contact)
        except KeyError as e:
            logging.error(e)
            self._set_response()
            self.wfile.write(("Missing required fields: " + str(e) + "\n").encode('utf-8'))
            raise KeyError(e)
        except Exception as e:
            logging.error(e)
            raise Exception(e)


    def handle_post(self):
        if self.path not in ALLOWED_PATHS:
            self._set_response()
            self.wfile.write(("Path not allowed: " + self.path + ".\nOnly \"" + '", "'.join(ALLOWED_PATHS) + "\" available.\n").encode('utf-8'))
            return
        if self.headers['Content-Type'] != "application/json":
            self._set_response()
            self.wfile.write(("Wrong Content-Type: " + self.headers['Content-Type'] + ".\nOnly \"application/json\" allowed.\n").encode('utf-8'))
            return
        post_data = json.loads(self.get_post_data())
        message = post_data.get('message')
        contacts = []
        if ALLOWED_PATHS[0] == self.path:
            contacts = [self.validate_contact(post_data).get('phone_number')]
        if ALLOWED_PATHS[1] == self.path:
            recipients = post_data.get('recipients')
            if len(recipients) > 1000:
                return self.json_response({ "message": "Too many recipients. Maximum allowed is 1000." }, 400)
            if not post_data.get('campaign_id'):
                return self.json_response({ "message": "Missing required fields: campaign_id" }, 400)
            for contact in recipients:
                contacts.append(self.validate_contact(contact).get('phone_number'))
        return self.json_response({ "message": "Sent an SMS with content '{}' to {}".format(message, ', '.join(contacts)) })


    def do_GET(self):
        self.do_log("GET")


    def do_POST(self):
        self.handle_post()


    def do_PUT(self):
        self.do_log("PUT")


    def do_DELETE(self):
        self.do_log("DELETE")


def run(address, port, server_class=HTTPServer, handler_class=S):
    logging.basicConfig(level=logging.INFO)
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd on ' + address + ':' + str(port) + '...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n" + sys.argv[0] + " [address] [port]")
        sys.exit(1)

    run(sys.argv[1], int(sys.argv[2]))
