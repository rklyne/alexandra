#! /usr/bin/env python

from alexandra import Alexandra
from sys import argv
from time import sleep

def do_tick(tick, alex):
    sleep(alex.config['tick_seconds'])
    alex.pubsub.publish('tick', tick + 1)

alex = Alexandra(argv[1])
tick_queue = alex.pubsub.subscribe('tick')
do_tick(0, alex)
alex.pubsub.consume_queue(tick_queue, lambda t: do_tick(t, alex))
