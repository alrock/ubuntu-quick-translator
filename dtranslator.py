import translator
import socket
import json
import sys
import os

if not translator.init():
	sys.exit(1)

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 55066              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
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