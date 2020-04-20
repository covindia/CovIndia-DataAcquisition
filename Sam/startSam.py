import tweepy
import json
import time
import requests

def getTokens():
	return json.load(open('res/TOKENS.json', 'r'))

def slack_tokens():
	return json.load(open('res/slackTokens.json', 'r'))

minutes = 1

auth = tweepy.OAuthHandler(getTokens()["API_key"], getTokens()["API_secret_key"])
auth.set_access_token(getTokens()["access_token"], getTokens()["access_token_secret"])

api = tweepy.API(auth, wait_on_rate_limit = True)

def sendReport(jsonData):

	response = requests.post(slack_tokens()["url"], json=jsonData, headers={'Content-Type': 'application/json'})

	if(response.status_code != 200):
		print("Failed to send message. Error : " + response.text)

def checkCase(text):
	text = text.lower()
	return (('covid' in text or 'coronavirus' in text) and ('fresh' in text or 'positive' in text or 'new case' in text or 'dead' in text or 'death' in text or 'deaths' in text or 'passed away' in text or 'dies' in text) or 'bulletin' in text)

def updateTweetsInfected():

	public_tweets = api.home_timeline()

	for tweet in public_tweets:

		if(checkCase(tweet.text)):

			try:
				tweet.retweet()
			
			except Exception as e:
				print('Exception : {}'.format(e))
				print('Tweet : {}\n\n'.format(tweet.text))

def main():

	print('Sam is up!')

	sendReport({'text': "Report: ", 'attachments' : [{'text' : "Gaining altitude, Sam ready to fly!"}]})

	update_time = 0

	try:
		while True:

			updateTweetsInfected()

			if(update_time == 15):
				sendReport({'text': "Update:", 'attachments' : [{'text' : "Update : Sam is still soaring the skies."}]})
				update_time = 0

			update_time += 1

			time.sleep(60 * minutes)
	
	except Exception as e:
		
		sendReport({'text': "Sam has crashed! <@" + slack_tokens()["mechanicID"] + "> manual restart required. Do it ASAP!", 'attachments' : [{'text' : "Exception : {}".format(e)}]})
		print('Sam crashed real hard. Error : {}'.format(e))
	
	# You don't wan't this to happen, it is very bad if it does, since Sam is our OP data-gatherer
	# Trust me, you'll want him, no matter what

if __name__ == '__main__':

	try:
		main()

	except KeyboardInterrupt:
		sendReport({'text': "Report: ", 'attachments' : [{'text' : "Sam has landed safely. Stopped manually."}]})
	
	except Exception as e:
		sendReport({'text': "Sam has crashed! <@" + slack_tokens()["mechanicID"] + "> manual restart required. Do it ASAP!", 'attachments' : [{'text' : "Exception : {}".format(e)}]})

# I'm not sure which Except will work, beacuse of the infinite While loop, let's see if we can figure it out

# Also, don't forget to checkout this video, cuz it's fun XD https://www.youtube.com/watch?v=dQw4w9WgXcQ