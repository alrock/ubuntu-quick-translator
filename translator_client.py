#!/usr/bin/env python

import translator
import socket
import json

HOST = 'localhost'        # The remote host
PORT = 55066             # The same port as used by the server
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.send(json.dumps({'auto': True}))
	s.close()
except socket.error:
	translator.notify('Translator', "Can't connect to server")
except TypeError:
	translator.notify('Translator', "Something terrible happens")
#print 'Received', repr(data)