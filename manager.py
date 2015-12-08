import argparse
import hashlib
import logging
import os
import gc
import re
import time
import signal
import traceback
# import resource
import sys

import gevent.event
import gevent.socket as socket
import greenlet
# from dateutil.tz import tzutc
import gevent.greenlet

try:
    import msgpack
except ImportError:
    msgpack = None

import logging  
log = logging.getLogger("server log")  

from notifier import NotificationThread
from user import UserThread
from web import WebThread


class Manager(object):
    """
    Manage 
    """

    def __init__(self):
        self._complete = gevent.event.Event()


        #1 
        self.notifier = NotificationThread(self)
        self.user = UserThread(self)
        self.web = WebThread(self)
        
        self.vms = {}
        self.ternimals = {}

    def delete_cluster(self, fs_id):
        """
        Note that the cluster will pop right back again if it's
        still sending heartbeats.
        """
        pass
        # victim = self.clusters[fs_id]
        # victim.stop()
        # victim.done.wait()
        # del self.clusters[fs_id]
        #
        # self._expunge(fs_id)

    def stop(self):
        log.info("%s stopping" % self.__class__.__name__)
        #2
        self.notifier.stop()
        self.user.stop()
        self.web.stop()
 

    def _expunge(self, fsid):

        pass


    def _recover(self):
        pass
        

    def start(self):
        log.info("%s starting" % self.__class__.__name__)

        # Before we start listening to the outside world, recover
        # our last known state from persistent storage
        try:
            self._recover()
        except:
            log.exception("Recovery failed")
            os._exit(-1)

        #3
        self.notifier.start()
        self.user.start()
        self.web.start()
        

    def join(self):
        log.info("%s joining" % self.__class__.__name__)
        #4
        self.notifier.join()
        self.user.join()
        self.web.join()
        

    def on_discovery(self, minion_id, heartbeat_data):
        log.info("on_discovery: {0}/{1}".format(minion_id, heartbeat_data['fsid']))
        


def dump_stacks():
    """
    This is for use in debugging, especially using manhole
    """
    for ob in gc.get_objects():
        if not isinstance(ob, greenlet.greenlet):
            continue
        if not ob:
            continue
        log.error(''.join(traceback.format_stack(ob.gr_frame)))


def main():
    

    m = Manager()
    m.start()

    complete = gevent.event.Event()

    def shutdown():
        log.info("Signal handler: stopping")
        complete.set()

    gevent.signal(signal.SIGTERM, shutdown)
    gevent.signal(signal.SIGINT, shutdown)

    while not complete.is_set():
        complete.wait(timeout=1)
main()