from slack import RTMClient
import time
import json
import getValues
import requests

def getTokens():
	allTokens = json.load(open('res/TOKENS.json', 'r'))
	return allTokens

@RTMClient.run_on(event="hello")
def bot_init(**payload):
	print('The bot has started to run\n')
	
@RTMClient.run_on(event="message")
def say_hello(**payload):
	data = payload['data']
	web_client = payload['web_client']

	message = ''
	channel_id = ''
	user = ''
	try:
		message = data['text']
		channel_id = data['channel']
		user = data['user']
	except:
		pass
	if(message.startswith('!')):
		if(message.startswith('!start')):
			web_client.chat_postMessage(channel = channel_id, text="Hi <@{}>! I'm still awake!".format(user))

		elif(message.startswith('!districtdata')):
			web_client.chat_postMessage(channel = channel_id, text="Here's the district-wise tally :\n{}".format(getValues.districtData()))

		elif(message.startswith('!statedata')):
			web_client.chat_postMessage(channel = channel_id, text="Here's the state-wise tally :\n{}".format(getValues.stateData()))

		elif(message.startswith('!apidata')):
			web_client.chat_postMessage(channel = channel_id, text="Here's the API data :\n{}".format(getValues.apiDistrictData()))

		elif(message.startswith('!findstate')):
			stateName = message[11:]
			if(len(stateName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.findState(stateName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the State")

		elif(message.startswith('!finddist')):
			districtName = message[10:]
			if(len(districtName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.findDistrict(districtName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the District")
		
		elif(message.startswith('!statedists')):
			stateName = message[12:]
			if(len(stateName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.stateDists(stateName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the State")

		elif(message.startswith('!distnatot')):
			web_client.chat_postMessage(channel = channel_id, text=getValues.totDistNA())

		elif(message.startswith('!distnastate')):
			stateName = message[13:]
			if(len(stateName) > 0):
				web_client.chat_postMessage(channel = channel_id, text=getValues.distNAstate(stateName))
			else:
				web_client.chat_postMessage(channel = channel_id, text="Enter the State")
		
		elif(message.startswith('!todaysdata')):
			web_client.chat_postMessage(channel = channel_id, text=getValues.getTodaysData())
		
		elif(message.startswith('!todaysstate')):
			web_client.chat_postMessage(channel = channel_id, text=getValues.getTodaysStateData())
		
		elif(message.startswith('!findtodaysstate')):
			stateName = message[17:]
			web_client.chat_postMessage(channel = channel_id, text=getValues.findTodaysState(stateName))
			
		elif(message.startswith('!help')):
			fileManager = open('res/bot_intro.txt', 'r')
			bot_intro = fileManager.read()
			fileManager.close()
			web_client.chat_postMessage(channel = channel_id, text=bot_intro)

		else:
			web_client.chat_postMessage(channel = channel_id, text="IDK that command, try !help")
	
	elif('boomer' in message.lower() and user != ''):
		requests.post('https://slack.com/api/files.upload', data={'token': getTokens()["slack_bot_token"], 'channels': [channel_id], 'title': 'The boomer burn'}, files={'file': open('res/ok_boomer.jpg', 'rb')})

rtm_client = RTMClient(token=getTokens()["slack_bot_token"])
rtm_client.start()

# TODO : today's total count