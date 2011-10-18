#!/usr/bin/env python

import translator
import socket
import json
import time
import sys
import os

from daemon import Daemon

class DTranslator(Daemon):
    def __init__(self, pid):
        Daemon.__init__(self, pid, '/dev/null', '/var/log/dtranslator.log', '/var/log/dtranslator.log')
        self.HOST = ''
        self.PORT = 55066

    def run(self):
        if not translator.init():
            return
        os.nice(10)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(10)
        while True:
            conn, addr = s.accept()
            print 'Connected by', addr
            while True:
                data = conn.recv(1024)
                if not data: break
                try:
                    query = json.loads(data)
                    if query['auto']:
                        translator.translate_selected()
                    else: 
                        translator.translate(query['text'], query['lang'])
                except TypeError, KeyError:
                    print 'Request is not valid.'
            conn.close()

 
if __name__ == "__main__":
    daemon = DTranslator('/tmp/dtranslator.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)