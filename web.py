
from gevent import monkey
monkey.patch_all()
import gevent.greenlet
import gevent.event
from gevent import sleep
from gevent.pywsgi import WSGIServer
import struct

import time

from flask import Flask





class WebThread(gevent.greenlet.Greenlet):
    """
    Responsible for:
     - Listening for Websockets clients connecting, and subscribing them
       to the ceph: topics
     - Publishing messages to Websockets topics on behalf of other
       python code.
    """
    def __init__(self, manager):
        super(WebThread, self).__init__()

        self._complete = gevent.event.Event()

        self._ready = gevent.event.Event()

        self._manager = manager

    def stop(self):
        self._complete.set()

    def publish(self, topic, message):
        self._ready.wait()

    def _run(self):
        self._ready.set()
        app = Flask(__name__)
        @app.route('/')
        def hello_world():
            return 'Hello World!'

        while not self._complete.is_set():
            try:
                WSGIServer(('', 5000), app).serve_forever()

            except:
                self._complete.wait(timeout=1)
                continue

