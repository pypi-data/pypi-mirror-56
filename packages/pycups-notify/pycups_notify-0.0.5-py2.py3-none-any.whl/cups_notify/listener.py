# -*- coding: utf-8 -*-

import socket
import threading
import os.path as osp
from contextlib import closing
from xml.etree import ElementTree
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    # Python 2.x fallback
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import cups
from cups_notify import LOGGER
from cups_notify import event


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('', 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock.getsockname()[1]


class NotificationHandler(BaseHTTPRequestHandler):

    def get_chunk_size(self):
        size_str = self.rfile.read(2)
        while size_str[-2:] != b"\r\n":
            size_str += self.rfile.read(1)
        return int(size_str[:-2], 16)

    def get_chunk_data(self, chunk_size):
        data = self.rfile.read(chunk_size)
        self.rfile.read(2)
        return data

    def log_request(self, code='-', size='-'):
        """Don't print HTTP requests.
        """
        pass

    def do_GET(self):
        """At the begining of the connection, CUPS server ask for existing
        RSS file. Don't know what is the reason...
        """
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_PUT(self):
        """Serve a PUT request and trasfert event to the callback.
        """
        chunk_size = self.get_chunk_size()
        if chunk_size == 0:
            LOGGER.warning("Notification without data received")
        else:
            chunk_data = self.get_chunk_data(chunk_size)
            root = ElementTree.fromstring(chunk_data.decode('utf-8'))

            evts = []
            for channel in root.iterfind('channel'):
                for item in reversed([e for e in channel.iterfind('item')]):
                    data = dict((elem.tag, elem.text) for elem in item.iter() if elem.text.strip())
                    evts.append(event.CupsEvent(data))

            if evts:
                self.server.notify(evts)

        self.send_response(200)
        self.end_headers()


class NotificationListerner(HTTPServer):

    def __init__(self, cups_conn, callback, filters=None, address='localhost'):
        HTTPServer.__init__(self, (address, find_free_port()), NotificationHandler)
        self._conn = cups_conn
        self._thread = None
        self._filters = filters or [event.CUPS_EVT_ALL]
        self._rss_uri = 'rss://{}:{}'.format(self.server_address[0], self.server_address[1])
        self._last_guid = -1
        self._callback = callback

    def start(self):
        """Start the notification server.
        """
        if self._thread:
            raise EnvironmentError("Server is already running")
        LOGGER.info("Starting RSS feed listener at %s", self._rss_uri)
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True
        self._thread.start()

        self.cancel_subscriptions()

        # Renew notifications subscription
        if osp.exists(cups.getServer()):
            hostname = 'localhost'
        else:
            hostname = cups.getServer()
        cups_uri = "ipp://{}:{}".format(hostname, cups.getPort())
        self._conn.createSubscription(cups_uri,
                                      recipient_uri=self._rss_uri,
                                      events=self._filters)

    def is_running(self):
        """Return True if the notification server is started.
        """
        if self._thread:
            return self._thread.is_alive()
        return False

    def notify(self, evts):
        """Call the callback for each new event. Events are filtered
        because CUPS server re-sends all previously sent events.
        """
        valid_evts = []
        for evt in evts:
            if evt.guid > self._last_guid:
                valid_evts.append(evt.guid)
                self._callback(evt)
        self._last_guid = max(valid_evts)

    def cancel_subscriptions(self):
        """Cancel all subscriptions related to the server URI.
        """
        try:
            for sub in self._conn.getSubscriptions(self._rss_uri):
                self._conn.cancelSubscription(sub['notify-subscription-id'])
        except cups.IPPError:
            pass

    def shutdown(self):
        """Stop the notification server.
        """
        if self.is_running():
            self.cancel_subscriptions()
            HTTPServer.shutdown(self)
            self._thread.join()
            self._thread = None
        # Close socket, can be opened event if thread not running
        self.server_close()
