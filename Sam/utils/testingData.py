"""
		Gathers Testing Data

		Author : Aman Agrawal
"""

import requests
from json import load, dump
import pandas as pd
import numpy as np
from utils.updateSheet import updateSheet, slack_tokens

def sendReport(jsonData): # Red Wing's maing job
	#Too lazy to write this everytime, hence make function, get even more lazy
	response = requests.post(slack_tokens()["testingData_url"], json=jsonData, headers={'Content-Type': 'application/json'})

	if(response.status_code != 200):
		print("Failed to send message. Error : " + response.text)

def updateTestingData(data_url):

	try:
		with open('res/testing-data.json', 'r') as FPtr:
			old_data = load(FPtr)
	except:
		print('This must be the first time your running the func ;)')
		old_data = {}

	source = requests.get(data_url).json()

	cols = ['updatedon','state','totaltested','source']
	df = pd.DataFrame(columns=cols)
	df2 = pd.DataFrame(columns=cols)

	for litem in source['states_tested_data']:
		ser = pd.Series(litem)
		if ser['state']=='Andaman and Nicobar Islands':
			ser['state']='Andaman and Nicobar'
		if ser['state']=='Odisha':
			ser['state']='Orissa'
		if ser['state']=='Dadra and Nagar Haveli and Daman and Diu':
			ser['state']='Dadra and Nagar Haveli'
		ser = ser[['updatedon','state','totaltested','source']]
		if ser['totaltested']=='':
			continue
		df = df.append(ser,ignore_index=True)

	i=0
	rang=df.index
	rang = list(rang)
	while i in rang:
		s = df.loc[i]['state']
		j = i
		while True:
			if df.loc[j]['state']==s and j<rang[-1]:
				j=j+1
			else:
				if j==rang[-1]:
					break
				j=j-1
				break
		df.loc[j]['totaltested']=int(df.loc[j]['totaltested'])
		df2 = df2.append(df.loc[j],ignore_index=True)
		i=j+1

	new_data = df2.to_dict('index')

	for key in list(new_data.keys()):
		k = str(key)
		new_data[k] = new_data[key]
		del new_data[key]
	
	if(old_data != new_data):

		report_text = ''

		for index in (new_data.keys() - old_data.keys()):
			
			report_text += '{} - {} - {} - {}\n'.format(new_data[index]["updatedon"], new_data[index]["state"], new_data[index]["totaltested"], new_data[index]["source"])
			
			update = [new_data[index]["updatedon"], '00:00', new_data[index]["state"], new_data[index]["totaltested"], '', new_data[index]["source"]]
			updateSheet(update)
		
		sendReport({'text': "Report:", 'attachments' : [{'text' : "I have completed updating the below data:\n" + report_text}]})
		print('Finised updating')
	
	with open('res/testing-data.json','w') as fp:
		dump(new_data,fp)