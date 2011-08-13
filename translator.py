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
pygtk.require('2.0')

gtrans_url = 'http://translate.google.ru/translate_a/t'
#?client=x&text={TEXT}&sl={LANG_FROM}&tl={LANG_TO}
language = {'ru': 'en', 'en': 'ru'}

def get_xsel_text(arg = '-p'):
	xsel = subprocess.Popen(['xsel', arg], stdout=subprocess.PIPE)
	return xsel.communicate()[0]
	
def get_selected_text():
	return get_xsel_text()	
	
def get_clipboard_text():
	return get_xsel_text('-b')
	
def notify(title, text, image = None):
	n = pynotify.Notification(title, text, image)
	if not n.show():
		print "Oops. Can't show notify."
		
def dnotify(text):
	notify('Translator', text, 'locale')
		
def send_request(text, tl):
	global gtrans_url
	text = get_selected_text();
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
			
			
def run():
	if not pynotify.init("Images Test"):
		sys.exit(1)
	
	text = get_selected_text()
	translate(text)
	

if __name__ == '__main__':
	run()
