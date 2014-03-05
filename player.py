from json import dumps, load, loads
from pubsub import create_channel, publish, subscribe, unsubscribe, get_message
from time import sleep
from sys import exit
from urllib2 import build_opener, HTTPHandler, Request, URLError, urlopen

IMAGE_FILE = 'player_image.png'

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def in_rect(self, rect):
        return rect.top_left._above_and_left_of(self) \
           and self._above_and_left_of(rect.bottom_right)

    def to_pair(self):
        return [self.x, self.y]

    def _above_and_left_of(self, vector):
        return self.x <= vector.x and self.y <= vector.y

class Rect:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def in_rect(self, rect):
        return self.top_left.in_rect(rect) and self.bottom_right.in_rect(rect)

    def move(self, v):
        return Rect(self.top_left.add(v), self.bottom_right.add(v))

def init():
    channel = create_channel()
    config = init_config(channel)
    publish_image(config['library_url'])
    rect = Rect(config['start'],
                config['start'].add(Vector(config['width'], config['height'])))
    send_position(rect.top_left, channel)
    commands_queue = subscribe(channel, 'commands.player')

    return channel, commands_queue, rect, config

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

    return {'start': Vector(config['player_start_x'], config['player_start_y']),
            'width': 50,
            'height': 50,
            'library_url': library_url,
            'tick': config['tick_seconds'],
            'deltas': {'left': Vector(-5, 0), 'right': Vector(5, 0),
                       'up': Vector(0, -5), 'down': Vector(0, 5)}}

def publish_image(library_url):
    image_data = open(IMAGE_FILE).read()
    opener = build_opener(HTTPHandler)
    request = Request(library_url + '/player/player_image.png', image_data)
    request.add_header('Content-Type', 'image/png')
    request.get_method = lambda: 'PUT'
    opener.open(request)

def main_loop(channel, commands_queue, rect, deltas, tick):
    while True:
        command = get_input(channel, commands_queue)
        if command:
            rect = do(command, rect, deltas)
        sleep(tick)

def do(command, rect, deltas):
    delta = deltas.get(command)
    if not delta:
        return rect
    new_rect = rect.move(delta)
    send_position(new_rect.top_left, channel)
    return new_rect

def send_position(position, channel):
    pair = position.to_pair()
    publish(channel, 'movement.player', dumps(pair))

def get_input(channel, commands_queue):
    message = get_message(channel, commands_queue)
    if message:
        return loads(message)
    else:
        return None

channel, commands_queue, rect, config = init()
main_loop(channel, commands_queue, rect, config['deltas'], config['tick'])
