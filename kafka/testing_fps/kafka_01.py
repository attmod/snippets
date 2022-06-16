#!/usr/bin/env python3

import kafka
from kafka import KafkaConsumer

import json
import time
import math

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



consumer = KafkaConsumer('events',
                         bootstrap_servers=[KAFKA_IP+':'+KAFKA_PORT])
for msg in consumer:
    """ ConsumerRecord:
    ConsumerRecord(topic='events',
                   partition=0,
                   offset=15,
                   timestamp=1645468388673,
                   timestamp_type=0,
                   key=None,
                   value=b'{"hello": "there"}',
                   headers=[],
                   checksum=None,
                   serialized_key_size=-1,
                   serialized_value_size=18,
                   serialized_header_size=-1)
    """


    a = json.loads( msg.value )



    if a['name'] not in codes.keys():
        # new code
        #codes['name'] = a['name']
        name = a['name']
        codes[name] = dict()
        codes[name]['payload'] = a['payload']
        codes[name]['health'] = 0
        codes[name]['health_timestamp'] = time.time()
        codes[name]['inhibit_time'] = 0
    
    name = a['name']

    # update health
    # first: natural decay
    newtime = time.time()
    newhealth = codes[name]['health']*math.exp(-0.6*(newtime-codes[name]['health_timestamp']))
    # print("decay {} down to {} after {}".format( codes[name]['health'], newhealth, newtime-codes[name]['health_timestamp']) )

    if 'inhibit' in a.keys():
        if a['inhibit'] != 0: # wide range, just make 'inhibit' appear in the raw code
            codes[name]['inhibit_time'] = time.time()

    if codes[name]['inhibit_time'] == 0:
        inh = 0
    else:
        inh = math.exp(-0.95*(newtime-codes[name]['inhibit_time']))

    if 'input' in a.keys() and a['input'] == 1:
        u = 1
    else:
        u = 0
    newhealth_ui = (newhealth + u*( (1-newhealth)*0.4)  )*(1-inh)
    # print("input/inhibit to {}".format(newhealth))

    print("code {} before {:.6f} after decay {:.6f} after input/inhibit {:.6f} transport delay of {}".format( name, codes[name]['health'], newhealth, newhealth_ui, time.time()-a['timestamp']))


    codes[name]['health'] = newhealth_ui
    codes[name]['health_timestamp'] = newtime

    #print(codes[name])

