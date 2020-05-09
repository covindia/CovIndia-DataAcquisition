import gspread
import json
import requests
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def getTokens():
	allTokens = json.load(open('res/TOKENS.json', 'r'))
	return allTokens

def getDate():
	return datetime.now().strftime('%d/%m/20%y')

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('res/credentials.json',scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(getTokens()["sheet_url"]).worksheet('Sheet1')

# DON'T EDIT ANYTHING ABOVE THIS!!
totalData = {} # has all the data
todaysData = {}
totalSumDead = 0
totalSumInfected = 0
rowCount = False
rowNum = 1
def reloadData():
	global rowCount
	global rowNum
	global totalSumDead
	global totalSumInfected
	global totalData
	global todaysData
	rowCount = False
	rowNum = 1
	totalSumDead = 0
	totalSumInfected = 0
	totalData = {}
	todaysData = {}
	for row in sheet.get():   #sheet.get the whole document as a list of lists

		if not rowCount:
			rowCount = not rowCount
			continue
		try:
			districtBoi = row[3]
			stateBoi = row[2]
			dateBoi = row[0]
		except Exception as e:
			print('Exception at {}, error : {}'.format(rowNum, e))

		if stateBoi in totalData:
			if districtBoi in totalData[stateBoi]:
				try:
					totalData[stateBoi][districtBoi]["infected"] += int(row[4])
				except:
					pass

				try:
					totalData[stateBoi][districtBoi]["dead"] += int(row[5])
				except:
					pass
			
			else:
				totalData[stateBoi][districtBoi] = {}
				try:
					totalData[stateBoi][districtBoi]["infected"] = int(row[4])
				except:
					totalData[stateBoi][districtBoi]["infected"] = 0

				try:
					totalData[stateBoi][districtBoi]["dead"] = int(row[5])
				except:
					totalData[stateBoi][districtBoi]["dead"] = 0
		
		else:
			totalData[stateBoi] = {}
			totalData[stateBoi][districtBoi] = {}
			try:
				totalData[stateBoi][districtBoi]["infected"] = int(row[4])
			except:
				totalData[stateBoi][districtBoi]["infected"] = 0

			try:
				totalData[stateBoi][districtBoi]["dead"] = int(row[5])
			except:
				totalData[stateBoi][districtBoi]["dead"] = 0
		
		if(dateBoi == getDate()):
			if stateBoi in todaysData:
				if districtBoi in todaysData[stateBoi]:
					try:
						todaysData[stateBoi][districtBoi]["infected"] += int(row[4])
					except:
						pass

					try:
						todaysData[stateBoi][districtBoi]["dead"] += int(row[5])
					except:
						pass

				else:
					todaysData[stateBoi][districtBoi] = {}
					try:
						todaysData[stateBoi][districtBoi]["infected"] = int(row[4])
					except:
						todaysData[stateBoi][districtBoi]["infected"] = 0
					
					try:
						todaysData[stateBoi][districtBoi]["dead"] = int(row[5])
					except:
						todaysData[stateBoi][districtBoi]["dead"] = 0
			
			else:
				todaysData[stateBoi] = {}
				todaysData[stateBoi][districtBoi] = {}
				try:
					todaysData[stateBoi][districtBoi]["infected"] = int(row[4])
				except:
					todaysData[stateBoi][districtBoi]["infected"] = 0

				try:
					todaysData[stateBoi][districtBoi]["dead"] = int(row[5])
				except:
					todaysData[stateBoi][districtBoi]["dead"] = 0
		
		rowNum += 1

	for boi in totalData:
		for distBoi in totalData[boi]:
			totalSumInfected += totalData[boi][distBoi]["infected"]
			totalSumDead += totalData[boi][distBoi]["dead"]

def stateData():
	reloadData()
	stateText = ''
	for stateBoi in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for districtBoi in totalData[stateBoi]:
			infectedStateSum += totalData[stateBoi][districtBoi]["infected"]
			deadStateSum += totalData[stateBoi][districtBoi]["dead"]
		stateText += stateBoi +'\nInfected : {}'.format(infectedStateSum) + '\nDead : {}\n\n'.format(deadStateSum)
	return stateText

def districtData():
	reloadData()
	districtText = ''
	for stateBoi in totalData:
		districtText += '{} :\n'.format(stateBoi)
		for distBoi in totalData[stateBoi]:
			districtText += distBoi + ':\nInfected : {}'.format(totalData[stateBoi][distBoi]["infected"]) + '\nDead : {}\n\n'.format(totalData[stateBoi][distBoi]["dead"])
	return districtText


def apiDistrictData():
	reloadData()
	districtAPIdata = requests.get(getTokens()["district_api_url"]).json()
	apiDataText = ''
	for districtBoi in districtAPIdata:
		apiDataText += districtBoi + '\nInfected : {}'.format(districtAPIdata[districtBoi]['infected']) + '\nDead : {}\n\n'.format(districtAPIdata[districtBoi]['dead'])
	apiDataText += "Total infected : {}\n".format(totalSumInfected) + "Total dead : {}".format(totalSumDead)
	return apiDataText

def findState(stateName):
	reloadData()
	stateText = ''
	if stateName in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for districtBoi in totalData[stateName]:
			infectedStateSum += totalData[stateName][districtBoi]["infected"]
			deadStateSum += totalData[stateName][districtBoi]["dead"]
		stateText = 'Values for {}:\n'.format(stateName) + 'Infected : {}\nDead : {}'.format(infectedStateSum, deadStateSum)
		return stateText
	return('{} not found, check spelling and try again'.format(stateName))

def findDistrict(districtName):
	reloadData()
	districtText = ''
	if(districtName == 'DIST_NA'):
		return 'Use !distnatot to get all DIST_NA, or !distnastate statename for a particular state'
	for stateBoi in totalData:
		if districtName in totalData[stateBoi]:
			districtText = 'Values for {}, {}:\n'.format(districtName, stateBoi) + '\nInfected : {}'.format(totalData[stateBoi][districtName]["infected"]) + '\nDead : {}'.format(totalData[stateBoi][districtName]["dead"])
			return districtText
	return('{} not found, check spelling and try again'.format(districtName))

def stateDists(stateName):
	reloadData()
	infectedSum = 0
	deadSum = 0
	stateDistrictsText = 'Districts with numbers in {}:\n'.format(stateName)
	if stateName in totalData:
		for districtBoi in totalData[stateName]:
			infectedSum += totalData[stateName][districtBoi]["infected"]
			deadSum += totalData[stateName][districtBoi]["dead"]
			stateDistrictsText += districtBoi +'\nInfected : {}\nDead : {}\n\n'.format(totalData[stateName][districtBoi]["infected"], totalData[stateName][districtBoi]["dead"])
		stateDistrictsText += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
		return stateDistrictsText
	return "Found nothing for {}".format(stateName)

def totDistNA():
	reloadData()
	retText = 'DIST_NAs statewise :\n'
	distNAinfected = 0
	distNAdead = 0
	for stateBoi in totalData:
		for districtBoi in totalData[stateBoi]:
			if(districtBoi == 'DIST_NA'):
				retText += 'In {}:\n'.format(stateBoi) + 'Infected : {}\nDead : {}\n\n'.format(totalData[stateBoi][districtBoi]["infected"], totalData[stateBoi][districtBoi]["dead"])
				distNAinfected += totalData[stateBoi][districtBoi]["infected"]
				distNAdead += totalData[stateBoi][districtBoi]["dead"]
	if(distNAdead != 0 and distNAinfected != 0):
		retText += 'Total DIST_NA count :\nInfected : {}\nDead : {}'.format(distNAinfected, distNAdead)
		return retText
	return 'Good News, ALL DIST_NA CLEARED!!! Party time'

def distNAstate(stateName):
	reloadData()
	text = 'DIST_NAs in {} :\n'.format(stateName)
	if(stateName in totalData):
		if("DIST_NA" in totalData[stateName]):
			text += 'Infected : {}\nDeath : {}'.format(totalData[stateName]['DIST_NA']["infected"], totalData[stateName]['DIST_NA']["dead"])
			return text
	return "Good news! No DIST_NA for {}".format(stateName)

def getTodaysData():
	reloadData()
	text = ''
	infectedSum = 0
	deadSum = 0
	for stateBoi in todaysData:
		text += 'In state {}:\n'.format(stateBoi)
		for districtBoi in todaysData[stateBoi]:
			infectedSum += todaysData[stateBoi][districtBoi]["infected"]
			deadSum += todaysData[stateBoi][districtBoi]["dead"]
			text += '{} :\nInfected : {}\nDead : {}\n\n'.format(districtBoi, todaysData[stateBoi][districtBoi]["infected"], todaysData[stateBoi][districtBoi]["dead"])
	text += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
	if(text != ''):
		return text
	return 'Nothing entered for today'

def getTodaysStateData():
	reloadData()
	text = ''
	infectedSum = 0
	deadSum = 0
	for stateBoi in todaysData:
		text += 'In {}:\n'.format(stateBoi)
		stateInfected = 0
		stateDead = 0
		for districtBoi in todaysData[stateBoi]:
			infectedSum += todaysData[stateBoi][districtBoi]["infected"]
			stateInfected += todaysData[stateBoi][districtBoi]["infected"]
			stateDead += todaysData[stateBoi][districtBoi]["dead"]
			deadSum += todaysData[stateBoi][districtBoi]["dead"]
		text += 'Infected : {}\nDead : {}\n\n'.format(stateInfected, stateDead)
	text += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
	if(text != ''):
		return text
	return 'Nothing entered for today'

def findTodaysState(stateName):
	reloadData()
	text = 'Todays data for {}\n'.format(stateName)
	infectedSum = 0
	deadSum = 0
	if stateName in todaysData:
		for districtBoi in todaysData[stateName]:
			infectedSum += todaysData[stateName][districtBoi]["infected"]
			deadSum += todaysData[stateName][districtBoi]["dead"]
			text += '{}:\nInfected : {}\nDead : {}\n\n'.format(districtBoi, todaysData[stateName][districtBoi]["infected"], todaysData[stateName][districtBoi]["dead"])
		text += 'Total infected today : {}\nTotal dead today : {}'.format(infectedSum, deadSum)
		return text
	
	return 'Nothing entered for {} today'.format(stateName)

def findTodaysDistrict(districtName):
	reloadData()
	text = 'Todays data for {}:\n'.format(districtName)
	for stateName in todaysData:
		if districtName in todaysData[stateName]:
			text += 'Infected : {}\nDead : {}'.format(todaysData[stateName][districtName]["infected"], todaysData[stateName][districtName]["dead"])
			return text

	return 'Nothing entered for {} today'.format(districtName)