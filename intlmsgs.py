import json

pomsgs = {}
current_locale='zhtw'
def initpo():
	f = open( 'zhtw.js')
	pomsgs[current_locale] = json.load( f)
	f.close()

def gettext( msgid):
	try:
		pomsg = pomsgs[current_locale]
		msg = pomsg[msgid]
	except KeyError:
		return msgid
	return msg

