#!/usr/bin/env python3

import platform
import socket

import os
HOSTNAME = os.environ.get('HOSTNAME')

from flask import Flask, send_file, Response
app = Flask(__name__)


@app.route('/')
def index():
    return 'index, use /platform for platform.node() and /socket for socket.gethostname(), or /hostname for env HOSTNAME'

@app.route('/platform')
def platformCALL():
    return platform.node()

@app.route('/socket')
def socketCALL():
    return socket.gethostname()

@app.route('/hostname')
def hostnameCALL():
    return HOSTNAME



if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8910)
