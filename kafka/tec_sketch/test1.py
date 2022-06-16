#!/usr/bin/env python3

"""  kafka loop testing

Goal is to see a proper loop mechanism between events_raw and events

Metadata:
JSON schema v0.1


"""


from confluent_kafka import Consumer, Producer
import time
import json



p = Producer( {'bootstrap.servers': '192.168.49.2:31343'} )
c = Consumer({
    'bootstrap.servers': '192.168.49.2:31343',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})
c.subscribe(['events_raw'])

# p.produce('events', key=b'blue', value=b'8')


while True:
    msg = c.poll(1.0)

    # skip calculations if no msg or an error
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    # main calculations:

    print(msg.value().decode('utf-8'))


c.close()

