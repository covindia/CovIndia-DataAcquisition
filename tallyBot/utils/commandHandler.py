"""
	Author: Srikar
"""

import utils.functions as funcs

def getName(cmd, message):
	return message[len(cmd) + 1 :]

def commandHandler(message, user):

	if(message.startswith('!start')):
			return ("Hi <@{}>! I'm still awake!".format(user))

	elif(message.startswith('!help')):
		fileManager = open('res/bot_intro.txt', 'r')
		bot_intro = fileManager.read()
		fileManager.close()
		return (bot_intro)

	# Old sheet commands

	elif(message.startswith('!Ddata')):
		return ("Here's the district-wise tally :\n{}".format(funcs.districtData()))

	elif(message.startswith('!Sdata')):
		return ("Here's the state-wise tally :\n{}".format(funcs.stateData()))

	elif(message.startswith('!FS')):
		return (funcs.findState(getName('!FS', message)))

	elif(message.startswith('!FD')):
		return (funcs.findState(getName('!FD', message)))

	elif(message.startswith('!SD')):
		return (funcs.findState(getName('!SD', message)))

	elif(message.startswith('!distnatot')):
		return (funcs.totDistNA())

	elif(message.startswith('!distnaS')):
		return (funcs.findState(getName('!distnaS', message)))

	elif(message.startswith('!Tdata')):
		return (funcs.getTodaysData())

	elif(message.startswith('!TS')):
		return (funcs.getTodaysStateData())

	elif(message.startswith('!FTS')):
		return (funcs.findState(getName('!FTS', message)))

	elif(message.startswith('!FTD')):
		return (funcs.findState(getName('!FTD', message)))
	
	# New sheet commands

	elif(message.startswith('!2Ddata')):
		return ("Here's the district-wise tally :\n{}".format(funcs.districtData('new')))

	elif(message.startswith('!2Sdata')):
		return ("Here's the state-wise tally :\n{}".format(funcs.stateData('new')))

	elif(message.startswith('!2FS')):
		return (funcs.findState(getName('!2FS', message), 'new'))

	elif(message.startswith('!2FD')):
		return (funcs.findState(getName('!2FD', message), 'new'))

	elif(message.startswith('!2SD')):
		return (funcs.findState(getName('!2SD', message), 'new'))

	elif(message.startswith('!2distnatot')):
		return (funcs.totDistNA('new'))

	elif(message.startswith('!2distnaS')):
		return (funcs.findState(getName('!2distnaS', message), 'new'))

	elif(message.startswith('!2Tdata')):
		return (funcs.getTodaysData('new'))

	elif(message.startswith('!2TS')):
		return (funcs.getTodaysStateData('new'))

	elif(message.startswith('!2FTS')):
		return (funcs.findState(getName('!2FTS', message)))

	elif(message.startswith('!2FTD')):
		return (funcs.findState(getName('!2FTD', message)))
	
	else:
		return ("IDK that command, try !help")