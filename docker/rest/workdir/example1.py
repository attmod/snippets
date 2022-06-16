#!/usr/bin/env python3

import json
from flask import Flask, request, jsonify

import time

app = Flask(__name__)

"""
implements standard get / put / post / delete behaviour

"""

@app.route('/', methods=['GET'])
def get_data():
    name = request.args.get('name')
    return jsonify({'requested_name':name, 'timestamp':time.time(), 'method':'get'})

@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    return jsonify({'requested_name':name, 'timestamp':time.time(), 'method':'put', 'payload':record})

@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    return jsonify({'requested_name':name, 'timestamp':time.time(), 'method':'post', 'payload':record})
    
@app.route('/', methods=['DELETE'])
def delte_record():
    record = json.loads(request.data)
    return jsonify({'requested_name':name, 'timestamp':time.time(), 'method':'delete', 'payload':record})

app.run(debug=True)
