## importing python modules and dependencies for this program
import csv, requests, json, shelve
import pandas as pd 


## This is the identified "target list" of RXCUI
albuterol_ndc_list = [901483, 359144, 901484, 359145, 1190225, 1190220, 836366, 836286, 1649961, 1649560,
745752, 746763, 859088, 745679, 801095, 801092, 247044, 582498, 226577, 104582, 248781, 386998, 307779, 351137,
104514, 755497, 352051, 351136, 199924, 630208, 1437704, 1437702, 1362214, 245314, 248066, 197316, 247840, 
108889, 153741, 197318, 153742, 392321]



## this function will take the python diction of ndc status and extract the 'active rxcui' by findinging the 
## most recent the end date of 'active rxcui'.  
## In some cases there are 3 or more activeRxcui listed for an NDC, this function will extract the most recent rxcui.
## Example input of ndc_history_list: 
##"ndcHistory":[{"activeRxcui":"1719225","originalRxcui":"1368050","startDate":"201303","endDate":"201511"},
##{"activeRxcui":"1719225","originalRxcui":"1719225","startDate":"201512","endDate":"201706"},
##{"activeRxcui":"1718962","originalRxcui":"545162","startDate":"200810","endDate":"200901"},
##{"activeRxcui":"1719225","originalRxcui":"795550","startDate":"200810","endDate":"201302"},
##{"activeRxcui":"1661332","originalRxcui":"545162","startDate":"200810","endDate":"200901"},
##{"activeRxcui":"1719222","originalRxcui":"545162","startDate":"200810","endDate":"200901"}]
## In this case we would return the RXCUI '1719225', since the endDate is 20170706
## The function will return a single RXCUI or the string "No Active RXCUI for this NDC"
def find_active_rxcui(ndc_history_list):
	potential_rxcui_list = []
	latest_date= 190001
	for each in ndc_history_list:
		if int(each['endDate']) > latest_date:
			latest_date = int(each['endDate'])
			potential_rxcui_list.append(each['activeRxcui'])
	l = [x for x in potential_rxcui_list if x != '']
	try:
		return l[-1]
	except:
		return "No Active Rxcui for this NDC"


## this function takes the ndc and checks if it is in the cache file, if not it makes an API call to get the ndc status from RxNorm
## after a new ndc is queried, the results are saved to a cache file.
## The function will return a text string containing the NDC status
## Example string: {"ndcStatus":{"status":"Active","comment":"","ndcHistory":[{"activeRxcui":"309054","originalRxcui":"309054",
##"startDate":"200801","endDate":"200808"},{"activeRxcui":"476576","originalRxcui":"476576","startDate":"200810","endDate":"201706"}]}}

def initial_ndc_query(test_ndc, cache_fobj):
	if test_ndc in cache_fobj:
		print("*** RETRIEVING data from the cached file for RXCUI ***")
		result = cache_fobj[test_ndc]
		return result
	else:
		n_search_url = 'https://rxnav.nlm.nih.gov/REST/ndcstatus.json?ndc=' + test_ndc
		n_status = requests.get(n_search_url)
		print("*** ADDING saved data to cache file for RXCUI ***")
		cache_fobj[test_ndc] = n_status.text
		return n_status.text

## this function takes the search results from the initial_ndc_query function and looks at the status
## If the status is 'alien' or 'unknown' it will check a data file containing NDC and drug names (created through manual research)
## If it is 'alien' or 'unknown' and not in the data file, no drug information can be determined.
## If it isn't 'alien' or 'unknown' it will check to see if the RXCUI is the cache file 
## If it's in the cache file it will grab the drug name, if not it makes an API call to get the drug name from the RXCUI
## after a new RXCUI is queried, the results are saved to a cache file
## The function returns the RXCUI, drug name, and NDC status
def get_RXCUI_info(search_results, test_ndc, rxcui_cache_fobj):
	status = search_results['ndcStatus']['status']
	if status == 'Alien' or status == 'Unknown':
		# if test_ndc in data:
		# 	print("Retrieving Manual NDC results")
		# 	rxcui = str(test_ndc)
		# 	drug_name = data[test_ndc]
		# else:
		print("*** Cannot locate Drug Name for this NDC. ***")
		rxcui = str(test_ndc)
		drug_name = "Unknown Drug"
		return (rxcui, drug_name, status)		
	else:
		rxcui_list= search_results['ndcStatus']['ndcHistory']
		rxcui = find_active_rxcui(rxcui_list)
		if rxcui in rxcui_cache_fobj:
			print("*** RETRIEVING Rxcui from cached file! ***")
			drug_name = rxcui_cache_fobj[rxcui]
			return (rxcui, drug_name, status)
		p_search_url = 'https://rxnav.nlm.nih.gov/REST/rxcui/' + str(rxcui)+ '/properties.json'
		p_properties = requests.get(p_search_url)
		RXCUI_properties = json.loads(p_properties.text)
		try:
			drug_name =RXCUI_properties['properties']['name']
		except:
			drug_name = "Unknown Drug"
		print("*** ADDING Rxcui to cached file. ***")
		rxcui_cache_fobj[rxcui] = drug_name
	return (rxcui, drug_name, status)

## set up empty lists to hold the old spreadsheet and line by line build up the final spreadsheet
full_row_list= []
updated_spreadsheet = []

## Set up cache file names
cache_fname = "cached_NDC_results"
cache_fobj = shelve.open(cache_fname)

rxcui_cache_fname = "cached_RXCUI_results"
rxcui_cache_fobj = shelve.open(rxcui_cache_fname)

## This would be a text file in json format that contains NDC-> drug name pairs from manual NDC research
## Not necessary step, but I added them since I looked up information on over 650 "unknown" NDC
unkown_data_file = "data.txt"

## open and load the information from the text file into a python dictionary (JSON object) to be used for matching
## 'unknown' or 'alien' NDC numbers
with open(unkown_data_file) as json_file:
	data = json.load(json_file)

#### Start of user interaction ####
## ask user for the name of the file with target ndc
ndcfilename = input("Enter the name of the text file with the target NDCs ")
try:
	ndcfile = open(ndcfilename + '.txt', "r")
	for ndc in ndcfile:
		albuterol_ndc_list.append(int(ndc.strip()))
except:
	print("Enter a valid text file name. (You do not need to include '.txt' at the end)")
	exit()

#Prompt user for filename
fname = input("Enter the CSV file you want to perform NDC lookup on: ")
try:
	ifile  = open(fname +'.csv')
except:
	print("Enter a valid CSV file name. (You do not need to include '.csv' at the end)")
	exit()

## csv module will "read" the entire csv file and save each row of data as a comma delimited list of lists
reader = csv.reader(ifile)
for row in reader:
	full_row_list.append(row)
ifile.close()

## Create the "Header Row" for the final spreadsheet with all original headers and 3 additional ones
updated_spreadsheet.append(full_row_list[0])
updated_spreadsheet[0].append('RXCUI')
updated_spreadsheet[0].append('Drug name')
updated_spreadsheet[0].append('Albuterol?')

## Generate a list on screen of all column headers
print("\n", "Column Headers:")
for each in range(len(updated_spreadsheet[0])):
	print(each+1, ":", updated_spreadsheet[0][each])

## User will indicate the number of the column which corresponds to NDC number
NDC = input("Type the number of the column containing the NDC number: ")
try:
	NDC = int(NDC)-1
except:
	print("You must enter a valid number corresponding to the column!")
	exit()

## set initial row count to 1 and number of failures (unknown drugs) to 0 for counting purposes
count = 1
fail= 0
## go through each row of data beginning with position 1 (actually second row of data [skip headers])
for ndc in full_row_list[1:]:
	test_ndc = ndc[NDC]
	print("\nTest NDC #", count, test_ndc)
## Logic added to pad zeros on the left to make an 11 digit number if the original number is <11 and >6
	if len(test_ndc) <11 and len(test_ndc) >6:
		test_ndc = test_ndc.rjust(11,'0')
## If the ndc is in the "unknown" python dictionary, indicate this is not from RxNorm and grab the drug name from the dictionary	
	if test_ndc in data:
		rxcui = "Not in RxNorm, manual match"
		drug_name = data[test_ndc]
		status = "Not in RxNorm"
		rxcui_results = (rxcui, drug_name, status)
## Otherwise run the intial_ndc_query function
	else:
		result = initial_ndc_query(test_ndc, cache_fobj= cache_fobj)
## the result will either come from the cache file or the API call.  It will be string containing NDC status information
## json.loads(result) will turn the string into a python dictionary (JSON object)
		search_results = json.loads(result)
## this python dictionary is sent along with the ndc to the get_RXCUI_info funtion.
## The function returns the RXCUI, drug name, and NDC status in a tuple which can be indexed
		rxcui_results = get_RXCUI_info(search_results, test_ndc, rxcui_cache_fobj= rxcui_cache_fobj)
	
## getting rxcui and ndc variable into type integer for list comparison
## it is possbile that rxcui or test_ndc could contain alphabet characters or be a string.  In this case changing th
## type to integer would cause the program to fail.  In these instances the rxcui or test_ndc is set to an arbitrary number
	try:
		rxcui = int(rxcui_results[0])
	except:
		rxcui = 999999
	try:
		new_ndc = int(test_ndc)
	except:
		new_ndc = 111111

## Adding results to the current row data
## this will append the rxcui to the "RXCUI" column in the final spreadsheet
	ndc.append(rxcui_results[0])
## this will append the drug name to the "Drug Name" column in the final spreadsheet
	ndc.append(rxcui_results[1])
## if the rxcui appears in the target list of RXCUI at the beginning of the program, put yes in the last column	
	if rxcui in albuterol_ndc_list:
		ndc.append("Yes")
## Otherwise, put no in the last column
	else:
		ndc.append("No")
## Adding row results to final spreadsheet
	updated_spreadsheet.append(ndc)
	count +=1
	if rxcui_results[1] == "Unknown Drug":
		fail +=1

## This step closes the two cache files to prevent corruption
cache_fobj.close()
rxcui_cache_fobj.close()

## The next four lines will calculate the match rate, total length of the final spreadsheet (number of rows)
## and display the information for the user as a rough output
match_rate = float(((count-fail)-1)/(count-1))
print("\n\nLength of updated spreadsheet: ", (len(updated_spreadsheet)-1))
print("NDC numbers without drug information found: ", fail)
print("Percent of NDC matching = ", match_rate)	
print("Used %s as the target file when analyzing NDC numbers which contains %s NDC numbers" %(ndcfilename, len(albuterol_ndc_list)))
## Generate a new CSV file with all original data plus 
## 3 new columns specifying RXCUI, Drug Name and whether or not it is in the target group of medications
## New CSV filename is created with the original file name + "_albuterol_results"
spreadsheet_filename = fname + '_albuterol_results.csv'
updated_dataframe = pd.DataFrame(updated_spreadsheet)
## Last line actually converts all the data into a CSV file and saves it in the same folder
updated_dataframe.to_csv(spreadsheet_filename, index= False, header= False)