"""
	Author: Srikar
"""

from utils.getData import retTodaysData, retTotalData

def stateData(sheet = 'old'):
	totalData = retTotalData(sheet)
	stateText = ''
	for stateBoi in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for districtBoi in totalData[stateBoi]:
			infectedStateSum += totalData[stateBoi][districtBoi]["infected"]
			deadStateSum += totalData[stateBoi][districtBoi]["dead"]
		stateText += stateBoi +'\nInfected : {}'.format(infectedStateSum) + '\nDead : {}\n\n'.format(deadStateSum)
	return stateText

def districtData(sheet = 'old'):
	totalData = retTotalData(sheet)
	districtText = ''
	for stateBoi in totalData:
		districtText += '{} :\n'.format(stateBoi)
		for distBoi in totalData[stateBoi]:
			districtText += distBoi + ':\nInfected : {}'.format(totalData[stateBoi][distBoi]["infected"]) + '\nDead : {}\n\n'.format(totalData[stateBoi][distBoi]["dead"])
	return districtText

def findState(stateName, sheet = 'old'):
	totalData = retTotalData(sheet)
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

def findDistrict(districtName, sheet = 'old'):
	totalData = retTotalData(sheet)
	districtText = ''
	if(districtName == 'DIST_NA'):
		return 'Use !distnatot to get all DIST_NA, or !distnastate statename for a particular state'
	for stateBoi in totalData:
		if districtName in totalData[stateBoi]:
			districtText = 'Values for {}, {}:\n'.format(districtName, stateBoi) + '\nInfected : {}'.format(totalData[stateBoi][districtName]["infected"]) + '\nDead : {}'.format(totalData[stateBoi][districtName]["dead"])
			return districtText
	return('{} not found, check spelling and try again'.format(districtName))

def stateDists(stateName, sheet = 'old'):
	totalData = retTotalData(sheet)
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

def totDistNA(sheet = 'old'):
	totalData = retTotalData(sheet)
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

def distNAstate(stateName, sheet = 'old'):
	totalData = retTotalData(sheet)
	text = 'DIST_NAs in {} :\n'.format(stateName)
	if(stateName in totalData):
		if("DIST_NA" in totalData[stateName]):
			text += 'Infected : {}\nDeath : {}'.format(totalData[stateName]['DIST_NA']["infected"], totalData[stateName]['DIST_NA']["dead"])
			return text
	return "Good news! No DIST_NA for {}".format(stateName)

def getTodaysData(sheet = 'old'):
	todaysData = retTodaysData(sheet)
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

def getTodaysStateData(sheet = 'old'):
	todaysData = retTodaysData(sheet)
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

def findTodaysState(stateName, sheet = 'old'):
	todaysData = retTodaysData(sheet)
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

def findTodaysDistrict(districtName, sheet = 'old'):
	todaysData = retTodaysData(sheet)
	text = 'Todays data for {}:\n'.format(districtName)
	for stateName in todaysData:
		if districtName in todaysData[stateName]:
			text += 'Infected : {}\nDead : {}'.format(todaysData[stateName][districtName]["infected"], todaysData[stateName][districtName]["dead"])
			return text

	return 'Nothing entered for {} today'.format(districtName)