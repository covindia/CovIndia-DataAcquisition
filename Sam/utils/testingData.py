"""
	Code to automatically update testing data. Took some time to make it.

	Author: Srikar
"""
import requests
from json import load, dump
from datetime import datetime
from utils.updateSheet import updateSheet, slack_tokens, getTotalData

def updateTestingData(data_url):

	try:
		with open('res/testing-data.json', 'r') as FPtr:
			old_data = load(FPtr)
	except:
		print('This must be the first time your running the func ;)')
		old_data = {}

	source = requests.get(data_url).json()["states_tested_data"]

	new_data = {}

	for data in source:
		# print(data)

		date = data['updatedon']

		if(not checkDate(date)):
			continue

		try:
			totTested = int(data['totaltested'])
		except:
			continue
		
		state = adaptState(data['state'])

		source = data['source1']

		if date in new_data:

			if state in new_data[date]:

				new_data[date][state]["totTested"] = totTested
				new_data[date][state]["source"] = source
			
			else:

				new_data[date][state] = {}
				new_data[date][state]["totTested"] = totTested
				new_data[date][state]["source"] = source

		
		else:

			new_data[date] = {}

			new_data[date][state] = {}
			
			new_data[date][state]["totTested"] = totTested
			new_data[date][state]["source"] = source
	
	
	if(old_data != new_data):

		report_text = ''

		for date in new_data:

			sheet_data = getTotalData()

			if date not in old_data:
				for state in new_data[date]:

					if state in sheet_data:
						if(new_data[date][state]['totTested'] - sheet_data[state] == 0):
							continue
						else:
							update = [date, '00:00', state, new_data[date][state]['totTested'] - sheet_data[state], '', new_data[date][state]['source']]
						
					else:
						update = [date, '00:00', state, new_data[date][state]['totTested'], '', new_data[date][state]['source']]
					
					updateSheet(update)
					report_text += '{} - {} - {} - {}\n'.format(update[0], update[2], update[3], update[5])

			else:

				if (set(new_data[date]) - set(old_data[date])) != set():

					for state in (set(new_data[date]) - set(old_data[date])):

						if state in sheet_data:
							if(new_data[date][state]['totTested'] - sheet_data[state] == 0):
								continue
							else:
								update = [date, '00:00', state, new_data[date][state]['totTested'] - sheet_data[state], '', new_data[date][state]['source']]
						
						else:
							update = [date, '00:00', state, new_data[date][state]['totTested'], '', new_data[date][state]['source']]
						
						updateSheet(update)
						report_text += '{} - {} - {} - {}\n'.format(update[0], update[2], update[3], update[5])
		
		if report_text == '':
			report_text = 'Finished syncing local DB'
		sendReport({'text': "Report:", 'attachments' : [{'text' : "I have completed updating the below data:\n" + report_text}]})
		print('Finised updating')
	
	with open('res/testing-data.json','w') as fp:
		dump(new_data,fp)

def sendReport(jsonData): # Red Wing's main job
	#Too lazy to write this everytime, hence make function, get even more lazy
	response = requests.post(slack_tokens()["testingData_url"], json=jsonData, headers={'Content-Type': 'application/json'})

	if(response.status_code != 200):
		print("Failed to send message. Error : " + response.text)

def checkDate(date_str):
	
	min_date = datetime.strptime('18/05/2020', '%d/%m/%Y')
	date = datetime.strptime(date_str, '%d/%m/%Y')

	return(date >= min_date)

def adaptState(state):

	if(state =='Andaman and Nicobar Islands'):
		return 'Andaman and Nicobar'
	
	elif(state =='Odisha'):
		return 'Orissa'
	
	elif(state =='Dadra and Nagar Haveli and Daman and Diu'):
		return 'Dadra and Nagar Haveli'
	
	return state