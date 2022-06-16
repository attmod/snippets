#!/usr/bin/env python3

import kafka
from kafka import KafkaProducer

import os
KAFKA_IP = os.environ.get('KAFKA_IP')
KAFKA_PORT = os.environ.get('KAFKA_PORT')

import json
import time

producer = KafkaProducer( bootstrap_servers=[KAFKA_IP+':'+KAFKA_PORT])

code_input = {"name":"red",
     "payload":"12",
     "input": 1}

code_inhibit = {"name":"red",
     "payload":"12",
     "inhibit": 1}

inputs = [ 1, 2, 6, 7, 9, 10, 11, 12]
inhibits = [9.5]

maxtime = 15
t_start = time.time()
t_end = t_start + maxtime

while time.time() < t_end:
    t_now = time.time() - t_start
    send_input = [ i for i in inputs if i < t_now ]
    if len(send_input) > 0:
        code_input['timestamp'] = time.time()
        producer.send('events_raw', json.dumps(code_input).encode())
        print("input sent at {}".format( t_now ) )
        for drop_input in send_input:
            inputs.remove(drop_input)

    send_inhibit = [ i for i in inhibits if i < t_now ]
    if len(send_inhibit) > 0:
        code_inhibit['timestamp'] = time.time()
        producer.send('events_raw', json.dumps(code_inhibit).encode())
        print("inhibit sent at {}".format( t_now ) )
        for drop_inhibit in send_inhibit:
            inhibits.remove(drop_inhibit)

    time.sleep(0.001)

## produce asynchronously with callbacks
#producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

## block until all async messages are sent
producer.flush()