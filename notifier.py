
import gevent.greenlet
import gevent.event
# import json
# import manager
import gevent.socket as socket
import struct
try:
    import zmq
except ImportError:
    zmq = None
import time

class NotificationThread(gevent.greenlet.Greenlet):
    """
    Responsible for:
     - Listening for Websockets clients connecting, and subscribing them
       to the ceph: topics
     - Publishing messages to Websockets topics on behalf of other
       python code.
    """
    def __init__(self, manager):
        super(NotificationThread, self).__init__()

        self._complete = gevent.event.Event()

        self._ready = gevent.event.Event()

        self._manager = manager

    def stop(self):
        self._complete.set()

    def publish(self, topic, message):
        self._ready.wait()


    def _run(self):
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 8001


        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', MCAST_PORT))
        mreq = struct.pack("=4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


        self._ready.set()

        while not self._complete.is_set():
            try:
                data, address = s.recvfrom(1024)
                t = data.split('|')
                if t[0] == 'V':
                    self._manager.vms[t[1]] = time.time()*100
                else:
                    self._manager.ternimals[t[1]] = int(time.time())*100

                print (t[0], t[1], address[0])
            except :
                self._complete.wait(timeout=1)
                continue

