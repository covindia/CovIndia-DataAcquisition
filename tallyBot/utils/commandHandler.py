"""
	Author: Srikar
"""

import utils.functions as funcs

def commandHandler(message, user):
	if(message.startswith('!start')):
			return ("Hi <@{}>! I'm still awake!".format(user))

	elif(message.startswith('!districtdata')):
		return ("Here's the district-wise tally :\n{}".format(funcs.districtData()))

	elif(message.startswith('!statedata')):
		return ("Here's the state-wise tally :\n{}".format(funcs.stateData()))

	elif(message.startswith('!findstate')):
		stateName = message[11:]
		if(len(stateName) > 0):
			return (funcs.findState(stateName))
		else:
			return ("Enter the State")

	elif(message.startswith('!finddist')):
		districtName = message[10:]
		if(len(districtName) > 0):
			return (funcs.findDistrict(districtName))
		else:
			return ("Enter the District")

	elif(message.startswith('!statedists')):
		stateName = message[12:]
		if(len(stateName) > 0):
			return (funcs.stateDists(stateName))
		else:
			return ("Enter the State")

	elif(message.startswith('!distnatot')):
		return (funcs.totDistNA())

	elif(message.startswith('!distnastate')):
		stateName = message[13:]
		if(len(stateName) > 0):
			return (funcs.distNAstate(stateName))
		else:
			return ("Enter the State")

	elif(message.startswith('!todaysdata')):
		return (funcs.getTodaysData())

	elif(message.startswith('!todaysstate')):
		return (funcs.getTodaysStateData())

	elif(message.startswith('!findtodaysstate')):
		stateName = message[17:]
		return (funcs.findTodaysState(stateName))

	elif(message.startswith('!findtodaysdist')):
		distName = message[16:]
		return (funcs.findTodaysDistrict(distName))
		
	elif(message.startswith('!help')):
		fileManager = open('res/bot_intro.txt', 'r')
		bot_intro = fileManager.read()
		fileManager.close()
		return (bot_intro)
	
	else:
		return ("IDK that command, try !help")