"""
	Code for our OP data gatherer Sam
	
	We also have Red Wing who always keeps an eye on Sam, his trusty owner

	Author: Srikar
"""
import tweepy
import json
import time
import requests
from utils.testingDataBot import getTestData

def getTokens():
	return json.load(open('res/TOKENS.json', 'r'))

def slack_tokens():
	return json.load(open('res/slackTokens.json', 'r'))

minutes = 1
antiCreepTime = 0

auth = tweepy.OAuthHandler(getTokens()["API_key"], getTokens()["API_secret_key"])
auth.set_access_token(getTokens()["access_token"], getTokens()["access_token_secret"])

api = tweepy.API(auth, wait_on_rate_limit = True)

def sendReport(jsonData): # Red Wing's maing job
	#Too lazy to write this everytime, hence make function, get even more lazy
	response = requests.post(slack_tokens()["url"], json=jsonData, headers={'Content-Type': 'application/json'})

	if(response.status_code != 200):
		print("Failed to send message. Error : " + response.text) #ideally this should never happen

def checkCase(text):
	text = text.lower()
	return (('covid' in text or 'coronavirus' in text) and ('fresh' in text or '+ve' in text or 'positive' in text or 'new case' in text or 'dead' in text or 'death' in text or 'passed away' in text or 'dies' in text or 'cured' in text or 'tested' in text or 'tests' in text or 'discharged' in text) or 'bulletin' in text)

def MPcase(text): # MP is weird, has everything in Hindi, this is the only english thing it had ;-;
	text = text.lower()
	return(('#mpfightscorona' in text) and ('#jansamparkmp' in text))

def updateTweetsInfected():
	
	global antiCreepTime  # It gets really creepy if Sam doesn't update us for a loong time, so 
	antiCreepTime += 1    # we have anti creep telling us that Sam is still out there, just not reporting nonsense :-)
	
	public_tweets = api.home_timeline()
	
	for tweet in public_tweets:

		if(checkCase(tweet.text) or MPcase(tweet.text)):

			try:
				tweet.retweet()
				antiCreepTime = 0
			
			except Exception as e:
				print('Exception : {}'.format(e))
				print('Tweet : {}\n\n'.format(tweet.text))
				
		elif(antiCreepTime == 25): # The actual code for antiCreep 
			sendReport({'text': "AntiCreep:", 'attachments' : [{'text' : "Sam is still scanning, last scan : " + tweet.text}]})
			antiCreepTime = 0

def main():

	print('Sam is up!')

	sendReport({'text': "Report: ", 'attachments' : [{'text' : "Gaining altitude, Sam ready to fly!"}]})

	update_time = 0

	try:
		while True:

			updateTweetsInfected()

			if(update_time == 60): # 60 is the minutes after which Red Wing will report about Sam's status
				sendReport({'text': "Report:", 'attachments' : [{'text' : "Update : Sam is still soaring the skies."}]})
				update_time = 0

			update_time += 1

			time.sleep(60 * minutes)
	
	except Exception as e:
		
		sendReport({'text': "Sam has crashed! <@" + slack_tokens()["mechanicID"] + "> restart required. Do it ASAP!", 'attachments' : [{'text' : "Exception : {}".format(e)}]})
		print('Sam crashed real hard. Error : {}'.format(e))
	
	# You don't wan't this to happen, it is very bad if it does, since Sam is our OP data-gatherer
	# Trust me, you'll want him, no matter what

	getTestData()

if __name__ == '__main__':

	try:
		main()

	except KeyboardInterrupt:
		sendReport({'text': "Report: ", 'attachments' : [{'text' : "Sam has landed safely. Stopped manually."}]})
	
	except Exception as e:
		sendReport({'text': "Sam has crashed! <@" + slack_tokens()["mechanicID"] + "> restart required. Do it ASAP!", 'attachments' : [{'text' : "Exception : {}".format(e)}]})


# I'm not sure which Except will work, beacuse of the infinite While loop, let's see if we can figure it out
# Just realised that both the excepts are important for catching different crashes so meh,  it's fine
# Also, don't forget to checkout this video, cuz it's fun XD https://www.youtube.com/watch?v=dQw4w9WgXcQ