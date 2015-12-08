

import gevent.greenlet
import gevent.event
# import json
# import manager
from gevent import sleep
import struct
try:
    import zmq
except ImportError:
    zmq = None
import time

class UserThread(gevent.greenlet.Greenlet):
    """
    Responsible for:
     - Listening for Websockets clients connecting, and subscribing them
       to the ceph: topics
     - Publishing messages to Websockets topics on behalf of other
       python code.
    """
    def __init__(self, manager):
        super(UserThread, self).__init__()

        self._complete = gevent.event.Event()

        self._ready = gevent.event.Event()

        self._manager = manager

    def stop(self):
        self._complete.set()

    def publish(self, topic, message):
        self._ready.wait()

    def _run(self):
        self._ready.set()

        while not self._complete.is_set():
            try:
                print self._manager.vms
                print self._manager.ternimals
                sleep(1)

            except:
                self._complete.wait(timeout=1)
                continue

