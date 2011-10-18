#!/usr/bin/env python

import sys
import subprocess
import pynotify
import gtk
import os
import urllib
import urllib2
import json
import pygtk
import time
pygtk.require('2.0')

gtrans_url = 'http://translate.google.ru/translate_a/t'
primary_lang = 'ru'
secondary_lang = 'en'

language = {primary_lang: secondary_lang, secondary_lang: primary_lang}

#-------------------begin-------------------------
# Code below was taken from append-hint-example.py
# http://notify-osd.sourcearchive.com/documentation/0.9.18/append-hint-example_8py-source.html

# Developers: even in Python this is globally nasty :), do something nicer in your own code
# Me: Oh, it's so difficult
capabilities = {'actions':                     False,
            'body':                            False,
            'body-hyperlinks':                 False,
            'body-images':                     False,
            'body-markup':                     False,
            'icon-multi':                      False,
            'icon-static':                     False,
            'sound':                           False,
            'image/svg+xml':                   False,
            'x-canonical-private-synchronous': False,
            'x-canonical-append':              False,
            'x-canonical-private-icon-only':   False,
            'x-canonical-truncation':          False}

def initCaps ():
	caps = pynotify.get_server_caps ()
	if caps is None:
		print "Failed to receive server caps."
		return False

	for cap in caps:
		capabilities[cap] = True
	return True

#-------------------end-------------------------

def get_xsel_text(arg = '-p'):
	xsel = subprocess.Popen(['xsel', arg], stdout=subprocess.PIPE)
	return xsel.communicate()[0]
	
def get_selected_text():
	return get_xsel_text()	
	
def get_clipboard_text():
	return get_xsel_text('-b')
	
def notify(title, text, image = None):
	global capabilities

	n = pynotify.Notification(title, text + '\n-----', image)
	if capabilities['x-canonical-append']:
		n.set_hint_string ("x-canonical-append", "allowed");
	else:
		print "The daemon does not support the x-canonical-append hint!"
	if not n.show():
		print "Oops. Can't show the notification."
	n.close()
		
def dnotify(text):
	notify('Translator', text, 'locale')
		
def send_request(text, tl):
	global gtrans_url
	#text = get_selected_text();
	query = urllib.urlencode((('client','x'),('tl',tl)))
	req = urllib2.Request(gtrans_url + '?' + query, urllib.urlencode((('text', text),)), 
	             	{'Host': 'www.google.com', 
	                 'User-Agent': 'Mozilla/5.0',
	                 'Accept-Encoding': 'deflate'})
	try:                
		res = urllib2.urlopen(req)
	except urllib2.URLError:
		dnotify("Error. Can't send request")
		sys.exit(1)
	return res
	
def translate(text, tl = 'ru'):
	global language;
	if text != None:
		res = send_request(text, tl)
		if res == None:
			dnotify("Error. Request failed")	
			return None
		obj = json.loads(res.read())
		try:
			if obj['src'] == tl:
				return translate(text, language[tl])
			trans = obj['sentences'][0]['trans']
			dnotify(trans)
			return trans	
		except KeyError, IndexError:
			dnotify("Error. Request failed (parse error)")	
			return None

def translate_selected():
	text = get_selected_text()
	translate(' '.join(text.split('\n')))

def init():
	if not pynotify.init("PyShortcutTranslator"):
		return False
	return initCaps()		
			
def run():
	if not init():
		sys.exit(1)
	translate_selected()

if __name__ == '__main__':
	run()
