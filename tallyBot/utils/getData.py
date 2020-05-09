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

def sendReport(jsonData): # This is Red Wing. Checkout Sam in the same repo for more info.
	#Too lazy to write this everytime, hence make function, get even more lazy
	response = requests.post(getTokens()["red_wing"], json=jsonData, headers={'Content-Type': 'application/json'})

	if(response.status_code != 200):
		print("Failed to send message. Error : " + response.text) #ideally this should never happen

def getDate(day):
	if(day == 'today'):
		return datetime.now().strftime('%d/%m/%Y')
	
	elif(day == 'yesterday'):
		yesterday = datetime.now() - timedelta(days = 1)
		return yesterday.strftime('%d/%m/%Y')

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)
client = gspread.authorize(creds)

old_sheet = client.open_by_url(getTokens()["old_sheet_url"]).worksheet('Sheet1')
new_sheet = client.open_by_url(getTokens()["new_sheet_url"]).worksheet('Sheet1')

def reloadData(sheet):

	totalData = {}
	todaysData = {}
	ystdData = {}

	data = sheet.get()   #sheet.get the whole document as a list of lists
	data = data[1:]

	rowNum = 1

	for row in data:

		try:
			date = row[0]
			state = row[2]
			district = row[3]
		
		except Exception as e:
			print('Exception at {}, error : {}'.format(rowNum, e))
			sendReport({'text': "Alert from TallyBot:", 'attachments' : [{'text' : "Somethings off at row {}. Exception: {}".format(rowNum, e)}]})

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
		
		if(date == getDate('today')):
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
		
		if(date == getDate('yesterday')):
			if state in todaysData:
				if district in todaysData[state]:
					
					ystdData[state][district]["infected"] += infected
					ystdData[state][district]["dead"] += dead
				
				else:
					ystdData[state][district] = {}
					
					ystdData[state][district]["infected"] = infected
					ystdData[state][district]["dead"] = dead
			
			else:
				ystdData[state] = {}
				ystdData[state][district] = {}
				
				ystdData[state][district]["infected"] = infected
				ystdData[state][district]["dead"] = dead
		rowNum += 1

	return ({
		"totalData" : totalData,
		"todaysData" : todaysData,
		"ystdData" : ystdData
	})

def retTotalData(sheet):
	if(sheet == 'new'):
		return reloadData(new_sheet)["totalData"]
	return reloadData(old_sheet)["totalData"]

def retTodaysData(sheet):
	if(sheet == 'new'):
		return reloadData(new_sheet)["todaysData"]
	return reloadData(old_sheet)["todaysData"]

def retYstdData(sheet):
	if(sheet == 'new'):
		return reloadData(new_sheet)["ystdData"]
	return reloadData(old_sheet)["ystdData"]