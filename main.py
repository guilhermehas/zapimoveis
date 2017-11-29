#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from urllib.parse import unquote
from robot import robot_execute
from threading import Thread
import os.path
import os

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        if self.path == '/':
            with open('index.html') as f:
                self.wfile.write(f.read().encode('utf-8'))
        elif self.path == '/reset':
            os.remove('out.txt')

        else:
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        post = post_data.decode('utf-8').split('=')[1]
        post = unquote(post)
        
        
        #s1 = "POST request,\n<br>Path:{}\n<br>Headers:\n<br>{}\n<br>\n<br>Body:<br>\n{}<br>\n".format(
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))
        #s2 = "POST request for {}".format(self.path)
        
        if os.path.isfile('./out.txt'):
            with open('out.txt') as f:
                self.wfile.write(f.read().encode('utf-8'))
        else:
            t = Thread(target = robot_execute, args = (post, ))
            t.start()
            self.wfile.write('iniciando robo'.encode('utf-8'))
        #t.run()

        #self.wfile.write(post.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

