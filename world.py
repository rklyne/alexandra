from json import dumps, load, loads
from pubsub import create_channel, publish, subscribe, unsubscribe, get_message
from time import sleep
from sys import exit
from urllib2 import URLError, urlopen

def init():
    channel = create_channel()
    config = init_config(channel)
    movement_queue = subscribe(channel, 'decision.movement.*')

    return channel, movement_queue, config

def init_config(channel):
    queue = subscribe(channel, 'library_url')
    sleep(1)
    library_url = get_message(channel, queue)
    if not library_url:
        print "No library url published, cannot fetch config"
        exit(1)
    unsubscribe(channel, queue, 'library_url')

    config_url = library_url + '/config.json'
    try:
        config_file = urlopen(config_url)
    except URLError:
        print "No config file at %s" % (config_url,)
        exit(1)
    config = load(config_file)

    return {'tick': config['tick_seconds']}

def main_loop(channel, movement_queue, tick):
    world = {}
    tick = 0
    while True:
        # increment and include tick
        # check for all movements
        movement = get_movement(channel, movement_queue)
        if movement is not None:
            entity, position = movement['entity'], movement['to']
            world[entity] = position
        publish(channel, 'world', dumps(world))
        sleep(tick)

def get_movement(channel, movement_queue):
    message = get_message(channel, movement_queue)
    if message is not None:
        return loads(message)
    else:
        return None

channel, movement_queue, config = init()
main_loop(channel, movement_queue, config['tick'])