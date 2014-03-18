#! /usr/bin/python

from alexandra import Alexandra
from json import dumps

IMAGE_FILE = 'player.png'
WIDTH = 50
HEIGHT = 50
DELTAS = {'left': (-5, 0), 'right': (5, 0), 'up': (0, -5), 'down': (0, 5)}

def init(alex):
    with open(IMAGE_FILE) as image_file:
        alex.enter_in_library(image_file.read(),
                              '/player/player.png', 'image/png')
    alex.enter_in_library(dumps({'width': WIDTH, 'height': HEIGHT}),
                          '/player/player.json', 'application/json')
    return alex.subscribe('commands.player')

def start_if_not_present(alex):
    if 'player_0' not in alex.world['entities']:
        position = (alex.config['player_start_x'],
                    alex.config['player_start_y'])
        send_movement(position, position, alex)

def move(command, alex):
    if 'player_0' not in alex.world['entities']:
        return
    position = alex.world['entities']['player_0']['position']
    new_position = apply_command(command, position)
    send_movement(position, new_position, alex)

def apply_command(command, position):
    delta = DELTAS.get(command, (0, 0))
    return (position[0] + delta[0], position[1] + delta[1])

def send_movement(from_position, to_position, alex):
    movement = {'entity': 'player', 'index': 0,
                'from': from_position, 'to': to_position}
    alex.publish('movement.player', movement)

alex = Alexandra(subscribe_world=True)
alex.on_each_tick(start_if_not_present)
commands_queue = init(alex)
alex.monitor(commands_queue, move)