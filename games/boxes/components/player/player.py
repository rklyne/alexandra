#! /usr/bin/env python

from alexandra import Alexandra
from json import dumps
from sys import argv

INDEX = int(argv[2])
NAME = 'player_%d' % (INDEX,)
WIDTH = 18
HEIGHT = 18
COLOUR = [0, 255, 255]
DELTAS = {'left': (-20, 0), 'right': (20, 0), 'up': (0, -20), 'down': (0, 20)}
MOVE_DELAY = 5

def init(alex):
    entity_data = {'width': WIDTH, 'height': HEIGHT, 'colour': COLOUR}
    alex.pubsub.publish('player/player.json', entity_data)
    return alex.pubsub.subscribe('commands.player')

def is_wall_construction(tick, movement):
    return movement['tick'] == tick-1 and movement['entity'].startswith('wall')

def walls_under_construction(tick, movements):
    return len(filter(lambda(m): is_wall_construction(tick, m), movements)) > 0

def update(tick, world, commands_queue, alex):
    if world is None \
      or walls_under_construction(world['tick'], world['movements'].values()):
        return

    world['tick'] = tick
    if NAME not in world['entities']:
        position = (alex.config['player_start_x'],
                    alex.config['player_start_y'])
        send_movement(position, position, world['tick'], alex)
    else:
        commands = alex.pubsub.get_all_messages(commands_queue)
        if len(commands) > 0:
            move(commands[-1], world, alex)

def move(command, world, alex):
    position = world['entities'][NAME]['position']
    new_position = apply_command(command, position)
    send_movement(position, new_position, world['tick'], alex)

def apply_command(command, position):
    delta = DELTAS.get(command, (0, 0))
    return (position[0] + delta[0], position[1] + delta[1])

def send_movement(from_position, to_position, tick, alex):
    movement = {'tick': tick,
                'entity': 'player', 'index': INDEX,
                'from': from_position, 'to': to_position}
    alex.pubsub.publish('movement.player', movement)

alex = Alexandra(argv[1])
commands_queue = init(alex)
world_monitor = alex.pubsub.make_topic_monitor('world')
alex.pubsub.consume_topic('tick', lambda t: update(t, world_monitor.latest(),
                                                   commands_queue, alex))
