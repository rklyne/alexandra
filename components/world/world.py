#! /usr/bin/python

from alexandra import Alexandra
from time import sleep

def main_loop(alex):
    movement_queue = alex.subscribe('decision_movement.*')
    world = {'tick': 0, 'entities': {}}
    while True:
        world['tick'] += 1
        for m in movement_queue.fetch_all():
            entity, index, position = m['entity'], m['index'], m['to']
            name = '%s_%d' % (entity, index)
            world['entities'][name] = {'entity': entity, 'position': position}
        alex.publish('world', world)
        sleep(alex.config['tick_seconds'])

main_loop(Alexandra())