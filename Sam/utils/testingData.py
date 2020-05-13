"""
		Gathers Testing Data

		Author : Aman Agrawal
"""

import requests
import json
import pandas as pd
import numpy as np

def getTestData():

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

	dic = df2.to_dict('index')
	with open('testing-data.json','w') as fp:
		json.dump(dic,fp,sort_keys=True,indent=4)
