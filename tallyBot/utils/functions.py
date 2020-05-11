"""
	Author: Srikar
"""

from utils.getData import retTodaysData, retTotalData, retYstdData, retDistNaData

def stateData(sheet = 'old'):
	totalData = retTotalData(sheet)
	stateText = ''
	for state in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for district in totalData[state]:
			infectedStateSum += totalData[state][district]["infected"]
			deadStateSum += totalData[state][district]["dead"]
		stateText += state +'\nInfected : {}'.format(infectedStateSum) + '\nDead : {}\n\n'.format(deadStateSum)
	return stateText

def districtData(sheet = 'old'):
	totalData = retTotalData(sheet)
	districtText = ''
	for state in totalData:
		districtText += '{} :\n'.format(state)
		for district in totalData[state]:
			districtText += district + ':\nInfected : {}'.format(totalData[state][district]["infected"]) + '\nDead : {}\n\n'.format(totalData[state][district]["dead"])
	return districtText

def findState(stateName, sheet = 'old'):
	totalData = retTotalData(sheet)
	stateText = ''
	if stateName in totalData:
		infectedStateSum = 0
		deadStateSum = 0
		for district in totalData[stateName]:
			infectedStateSum += totalData[stateName][district]["infected"]
			deadStateSum += totalData[stateName][district]["dead"]
		stateText = 'Values for {}:\n'.format(stateName) + 'Infected : {}\nDead : {}'.format(infectedStateSum, deadStateSum)
		return stateText
	return('{} not found, check spelling and try again'.format(stateName))

def findDistrict(districtName, sheet = 'old'):
	totalData = retTotalData(sheet)
	districtText = ''
	if(districtName == 'DIST_NA'):
		return 'Use !distnatot to get all DIST_NA, or !distnastate statename for a particular state'
	for state in totalData:
		if districtName in totalData[state]:
			districtText = 'Values for {}, {}:\n'.format(districtName, state) + '\nInfected : {}'.format(totalData[state][districtName]["infected"]) + '\nDead : {}'.format(totalData[state][districtName]["dead"])
			return districtText
	return('{} not found, check spelling and try again'.format(districtName))

def stateDists(stateName, sheet = 'old'):
	totalData = retTotalData(sheet)
	infectedSum = 0
	deadSum = 0
	stateDistrictsText = 'Districts with numbers in {}:\n'.format(stateName)
	if stateName in totalData:
		for district in totalData[stateName]:
			infectedSum += totalData[stateName][district]["infected"]
			deadSum += totalData[stateName][district]["dead"]
			stateDistrictsText += district +'\nInfected : {}\nDead : {}\n\n'.format(totalData[stateName][district]["infected"], totalData[stateName][district]["dead"])
		stateDistrictsText += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
		return stateDistrictsText
	return "Found nothing for {}".format(stateName)

def totDistNA(sheet = 'old'):
	totalData = retTotalData(sheet)
	retText = 'DIST_NAs statewise :\n'
	distNAinfected = 0
	distNAdead = 0
	for state in totalData:
		for district in totalData[state]:
			if(district == 'DIST_NA'):
				retText += 'In {}:\n'.format(state) + 'Infected : {}\nDead : {}\n\n'.format(totalData[state][district]["infected"], totalData[state][district]["dead"])
				distNAinfected += totalData[state][district]["infected"]
				distNAdead += totalData[state][district]["dead"]
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
	for state in todaysData:
		text += 'In state {}:\n'.format(state)
		for district in todaysData[state]:
			infectedSum += todaysData[state][district]["infected"]
			deadSum += todaysData[state][district]["dead"]
			text += '{} :\nInfected : {}\nDead : {}\n\n'.format(district, todaysData[state][district]["infected"], todaysData[state][district]["dead"])
	text += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
	if(text != ''):
		return text
	return 'Nothing entered for today'

def getTodaysStateData(sheet = 'old'):
	todaysData = retTodaysData(sheet)
	text = ''
	infectedSum = 0
	deadSum = 0
	for state in todaysData:
		text += 'In {}:\n'.format(state)
		stateInfected = 0
		stateDead = 0
		for district in todaysData[state]:
			infectedSum += todaysData[state][district]["infected"]
			stateInfected += todaysData[state][district]["infected"]
			stateDead += todaysData[state][district]["dead"]
			deadSum += todaysData[state][district]["dead"]
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
		for district in todaysData[stateName]:
			infectedSum += todaysData[stateName][district]["infected"]
			deadSum += todaysData[stateName][district]["dead"]
			text += '{}:\nInfected : {}\nDead : {}\n\n'.format(district, todaysData[stateName][district]["infected"], todaysData[stateName][district]["dead"])
		text += 'Total infected today : {}\nTotal dead today : {}'.format(infectedSum, deadSum)
		return text
	
	return 'Nothing entered in {} for today'.format(stateName)

def findTodaysDistrict(districtName, sheet = 'old'):
	todaysData = retTodaysData(sheet)
	text = 'Todays data for {}:\n'.format(districtName)
	for stateName in todaysData:
		if districtName in todaysData[stateName]:
			text += 'Infected : {}\nDead : {}'.format(todaysData[stateName][districtName]["infected"], todaysData[stateName][districtName]["dead"])
			return text

	return 'Nothing entered in {} for today'.format(districtName)

def getYstdData(sheet = 'old'):
	ystdData = retYstdData(sheet)
	text = ''
	infectedSum = 0
	deadSum = 0
	for state in ystdData:
		text += 'In state {}:\n'.format(state)
		for district in ystdData[state]:
			infectedSum += ystdData[state][district]["infected"]
			deadSum += ystdData[state][district]["dead"]
			text += '{} :\nInfected : {}\nDead : {}\n\n'.format(district, ystdData[state][district]["infected"], ystdData[state][district]["dead"])
	text += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
	if(text != ''):
		return text
	return 'Nothing entered yesterday'

def getYstdStateData(sheet = 'old'):
	ystdData = retYstdData(sheet)
	text = ''
	infectedSum = 0
	deadSum = 0
	for state in ystdData:
		text += 'In {}:\n'.format(state)
		stateInfected = 0
		stateDead = 0
		for district in ystdData[state]:
			infectedSum += ystdData[state][district]["infected"]
			stateInfected += ystdData[state][district]["infected"]
			stateDead += ystdData[state][district]["dead"]
			deadSum += ystdData[state][district]["dead"]
		text += 'Infected : {}\nDead : {}\n\n'.format(stateInfected, stateDead)
	text += 'Total infected : {}\nTotal dead : {}'.format(infectedSum, deadSum)
	if(text != ''):
		return text    # I'm pretty sure the below statement would be never used. If it is, that's good news!
	return 'Nothing entered yesterday'

def findYstdState(stateName, sheet = 'old'):
	ystdData = retYstdData(sheet)
	text = 'Yesterdays data for {}\n'.format(stateName)
	infectedSum = 0
	deadSum = 0
	if stateName in ystdData:
		for district in ystdData[stateName]:
			infectedSum += ystdData[stateName][district]["infected"]
			deadSum += ystdData[stateName][district]["dead"]
			text += '{}:\nInfected : {}\nDead : {}\n\n'.format(district, ystdData[stateName][district]["infected"], ystdData[stateName][district]["dead"])
		text += 'Total infected today : {}\nTotal dead today : {}'.format(infectedSum, deadSum)
		return text
	
	return 'Nothing was entered for {} yesterday'.format(stateName)

def findYstdDistrict(districtName, sheet = 'old'):
	ystdData = retYstdData(sheet)
	text = 'Yesterdays data for {}:\n'.format(districtName)
	for stateName in ystdData:
		if districtName in ystdData[stateName]:
			text += 'Infected : {}\nDead : {}'.format(ystdData[stateName][districtName]["infected"], ystdData[stateName][districtName]["dead"])
			return text

	return 'Nothing was entered in {} yesterday'.format(districtName)

def isSynced():
	old_sheet_data = retTotalData('old')
	new_sheet_data = retTotalData('new')

	old_infected_count = new_infected_count = 0
	old_dead_count = new_dead_count = 0

	for state in old_sheet_data:
		for district in old_sheet_data[state]:
			old_infected_count += old_sheet_data[state][district]["infected"]
			old_dead_count += old_sheet_data[state][district]["dead"]
	
	for state in new_sheet_data:
		for district in new_sheet_data[state]:
			new_infected_count += new_sheet_data[state][district]["infected"]
			new_dead_count += new_sheet_data[state][district]["dead"]

	if(old_infected_count == new_infected_count and old_dead_count == new_dead_count):
		return 'Old and new sheets match perfectly!'
	
	else:

		if(old_infected_count >= new_infected_count):

			if(old_dead_count > new_dead_count):
				return 'Old sheet has {} more infected cases and {} more death cases'.format(old_infected_count - new_infected_count, old_dead_count - new_dead_count)
			
			elif(old_dead_count == new_dead_count):
				return 'Old sheet has {} more infected cases. Death count matches'.format(old_infected_count - new_infected_count)
			
			else:
				return 'Old sheet has {} more infected cases and a deficit of {} death cases'.format(old_infected_count - new_infected_count, new_dead_count - old_dead_count)
			
		else:

			if(new_dead_count > new_dead_count):
				return 'New sheet has {} more infected cases and {} more death cases'.format(new_infected_count - old_infected_count, new_dead_count - old_dead_count)
			
			elif(new_dead_count == new_dead_count):
				return 'New sheet has {} more infected cases. Death count matches'.format(new_infected_count - old_infected_count)
			
			else:
				return 'New sheet has {} more infected cases and a deficit of {} death cases'.format(new_infected_count - old_infected_count, new_dead_count - old_dead_count)

def getDistNArows(stateName, sheet = 'old'):
	sheet_data = retDistNaData(sheet)
	text = 'Following are the rows for DIST_NA in {}\n'.format(stateName)
	
	if stateName in sheet_data:
		text += str(sheet_data[stateName])
	
	else:
		text = 'No DIST_NA in ' + stateName
	
	return text