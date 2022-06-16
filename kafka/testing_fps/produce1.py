#!/usr/bin/env python3

import kafka
from kafka import KafkaProducer

import os
KAFKA_IP = os.environ.get('KAFKA_IP')
KAFKA_PORT = os.environ.get('KAFKA_PORT')

import json
import time
import random

producer = KafkaProducer( bootstrap_servers=[KAFKA_IP+':'+KAFKA_PORT])




groups = ['colour']*3 + ['item']*2 + ['action']*1 + ['distractor']*15

group = dict()
group['colour'] = ['red']*4 + ['blue']*1 + ['green']*2
group['item'] = ['table']*10 + ['wood']*2 + ['hammer']*3 + ['cup']*4 + ['orange']*1 + ['apple']*1
group['distractor'] = ['d1']
group['action'] = ['point']

code_input = {"name":"",
     "payload":"",
     "input": 1}

fps = 30
try:
    while True:
        t_start = time.time()
        
        code_input['timestamp'] = time.time()
        gr = random.choice(groups)
        code_input['name'] = random.choice( group[gr] )
        code_input['payload'] = random.random()
        producer.send('events', json.dumps(code_input).encode())

        producer.flush() # force send
        t_now = time.time()

        # the random part is 5% noise for uneven wait times
        waittime = 1.0/fps - (t_now - t_start) +  (1.0/fps)*0.05*random.random()
        if waittime > 0:
            time.sleep(waittime)
        print(code_input, waittime)
except KeyboardInterrupt:
    print("caught ctrl-c")
    print("gently quitting")
## produce asynchronously with callbacks
#producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

## block until all async messages are sent
producer.flush()