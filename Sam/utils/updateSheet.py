"""
	Module to automatically update testing data on our DB.
	gspread is indeed cool. 

	Author: Srikar
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from json import load

def getTokens():
	return load(open('res/TOKENS.json', 'r'))

def slack_tokens():
	return load(open('res/slackTokens.json', 'r'))

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope) # hidden, it's a secret

client = gspread.authorize(creds)

sheet = client.open_by_url(getTokens()["sheet_url"]).worksheet('Sheet1')  # till here all gspread API stuff

def updateSheet(updateList):
	"""
		I must say this, append_row saved about 40 lines of code, and is more efficient.
		Should have found about this when Sauron was made. Meh, better late than never.
	"""
	sheet.append_row(updateList)