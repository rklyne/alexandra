from json import dumps, load, loads
from pubsub import create_channel, publish, subscribe, unsubscribe, \
                   get_message, get_all_messages, get_message_block
from StringIO import StringIO
from urllib2 import urlopen

class Queue:
    def __init__(self, channel, topic):
        self._channel = channel
        self._q = subscribe(self._channel, topic)

    def fetch_all(self):
        return map(loads, get_all_messages(self._channel, self._q))

class Alexandra:
    def __init__(self):
        self._channel = create_channel()
        self._library_url = self._get_library_url()
        self.config = self._get_config()
        self.world = None
        self.world_queue = None

    def subscribe(self, topic):
        return Queue(self._channel, topic)

    def publish(self, topic, message):
        publish(self._channel, topic, dumps(message))

    def next_tick(self):
        if self.world_queue is None:
            self.world_queue = subscribe(self._channel, 'world')
        self.world = loads(get_message_block(self._channel, self.world_queue))

    def get_library_file(self, path):
        url = self._library_url + path
        return StringIO(urlopen(url).read())

    def _get_library_url(self):
        library_url_queue = subscribe(self._channel, 'library_url')
        library_url = get_message_block(self._channel, library_url_queue)
        unsubscribe(self._channel, library_url_queue, 'library_url')
        return library_url

    def _get_config(self):
        return load(self.get_library_file('/config.json'))
