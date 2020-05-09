"""
	The bot that notified us of the 1.8K unknown district count.
	The core product of laziness.
	Author: Srikar
"""

from slack import RTMClient
import time
import json
import requests

from utils.commandHandler import commandHandler
from utils.getData import getTokens

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
		web_client.chat_postMessage(channel = channel_id, text=commandHandler(message, user))
	
	elif('boomer' in message.lower() and user != ''):
		requests.post('https://slack.com/api/files.upload', data={'token': getTokens()["slack_bot_token"], 'channels': [channel_id], 'title': 'The boomer burn'}, files={'file': open('res/ok_boomer.jpg', 'rb')})

rtm_client = RTMClient(token=getTokens()["slack_bot_token"])
rtm_client.start()

# TODO : change api function name
# TODO : add commands for new sheet
# TODO : add find Yesterday's state command