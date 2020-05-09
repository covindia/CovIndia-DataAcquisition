"""
	Author: Srikar
"""

import gspread
import json
import requests
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

def getTokens():
	return json.load(open('res/TOKENS.json', 'r'))

def getDate():
	return datetime.now().strftime('%d/%m/%Y')
	# today = datetime.now()
	# yesterday = today - timedelta(days = 1)

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(getTokens()["old_sheet_url"]).worksheet('Sheet1')

def reloadData():

	totalData = {}
	todaysData = {}

	data = sheet.get()   #sheet.get the whole document as a list of lists
	data = data[1:]

	rowNum = 1

	yesterdaysData = {}

	for row in data:

		try:
			date = row[0]
			state = row[2]
			district = row[3]
		
		except Exception as e:
			print('Exception at {}, error : {}'.format(rowNum, e))
			# TODO : Send a messae via Sam

		try:
			infected = int(row[4])
		except:
			infected = 0
		
		try:
			dead = int(row[5])
		except:
			dead = 0

		if state in totalData:
			if district in totalData[state]:

				totalData[state][district]["infected"] += infected
				totalData[state][district]["dead"] += dead
			
			else:
				totalData[state][district] = {}

				totalData[state][district]["infected"] = infected
				totalData[state][district]["dead"] = dead
		
		else:
			totalData[state] = {}
			totalData[state][district] = {}
			
			totalData[state][district]["infected"] = infected
			totalData[state][district]["dead"] = dead
		
		if(date == getDate()):
			if state in todaysData:
				if district in todaysData[state]:
					
					todaysData[state][district]["infected"] += infected
					todaysData[state][district]["dead"] += dead
				
				else:
					todaysData[state][district] = {}
					
					todaysData[state][district]["infected"] = infected
					todaysData[state][district]["dead"] = dead
			
			else:
				todaysData[state] = {}
				todaysData[state][district] = {}
				
				todaysData[state][district]["infected"] = infected
				todaysData[state][district]["dead"] = dead
		
		rowNum += 1

	return ({
		"totalData" : totalData,
		"todaysData" : todaysData
	})

def retTotalData():
	return reloadData()["totalData"]

def retTodaysData():
	return reloadData()["todaysData"]