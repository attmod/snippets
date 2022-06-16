#!/usr/bin/env python3

import kafka
from kafka import KafkaConsumer, KafkaProducer

import json
import time
import math
import yaml

import os
KAFKA_IP = os.environ.get('KAFKA_IP')
KAFKA_PORT = os.environ.get('KAFKA_PORT')

codes = dict()
inhibited = dict()

"""
    code schema for events_raw

    name:
    payload:
    


    code schema for event:
    name:
    payload:
    health:
    health_timestamp:
    inhibit_time:

"""

def age(codes,name):
    newtime = time.time()
    newhealth = codes[name]['health']*math.exp(-0.6*(newtime-codes[name]['health_timestamp']))

    code = codes[name]
    code['health'] = newhealth
    code['health_timestamp'] = newtime

    return code



with open("integrate1.yaml","r") as file:
    db = yaml.load(file,Loader=yaml.Loader)

producer = KafkaProducer( bootstrap_servers=[KAFKA_IP+':'+KAFKA_PORT])

consumer = KafkaConsumer('events',
                         bootstrap_servers=[KAFKA_IP+':'+KAFKA_PORT])

codes = dict()
now = time.time()
for values in db.values():
    for val in values:
        codes[val] = {'name':val,'health':0,'health_timestamp':now}
print(codes)
print("waiting")

try:
    while True:
        partitions = consumer.poll(100) # dictionary
        updates = []
        if len(partitions) > 0:
            for part in partitions:
                for msg in partitions[part]:
                    a = json.loads( msg.value )
                    codes[ a['name'] ] = a
                    updates.append( a['name'] )

        for name in updates:
            for eventfile in db:
                if name in db[eventfile]:
                    for partial_name in db[eventfile]:
                        codes['name'] = age(codes,partial_name)
                    active = [ name for name in db[eventfile] if codes[name]['health'] > 0.05 ]
                    if len(active) == len(db[eventfile]):
                        newcode = dict()
                        newcode['name'] = eventfile
                        newcode['timestamp'] = time.time()
                        newcode['input'] = 1
                        newcode['payload'] = 0
                        producer.send('events_raw', json.dumps(newcode).encode())
                        print(newcode)
            producer.flush()

        # TODO age the messages using decay?


        #producer.send('events', json.dumps(codes[name]).encode())
except KeyboardInterrupt:
    print("caught ctrl-c")
    print("gently quitting")

