#! /usr/bin/python

from json import load, dumps
from os.path import join as pathjoin
from pubsub import connect
from sys import argv
from time import sleep
from urllib2 import URLError, urlopen

def is_responsive(url):
    try:
        urlopen(url).read()
        return True
    except URLError:
        return False

def publish_url(host, port):
    game_id = argv[2]
    connection = connect('amqp://localhost', game_id)
    url = 'http://%s:%d' % (host, port)

    while is_responsive(url + '/index.html'):
        connection.publish(topic='library_url', message=dumps(url))
        sleep(1)

config_dir = argv[1]
config_file_path = pathjoin(config_dir, 'infra.json')
with open(config_file_path, 'r') as config_file:
    config = load(config_file)
host, port = config['library_host'], config['library_port']
publish_url(host, port)
