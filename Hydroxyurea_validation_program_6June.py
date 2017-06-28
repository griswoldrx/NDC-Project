0import csv 
import pandas as pd 
import requests 
import json 
import pickle
import shelve

hydroxyurea_rxcui_list = [105602, 197797, 200342, 200343, 200344, 213282,
213283, 213284, 283475]

def find_active_rxcui(ndc_history_list):
	potential_rxcui_list = []
	for each in ndc_history_list:
		potential_rxcui_list.append(each['activeRxcui'])
	l = [str(x) for x in potential_rxcui_list if x != '']
	try:
		return l[0]
	except:
		return "No Active Rxcui for this NDC"

def initial_ndc_query(test_ndc, cache_fname):
	cache_fobj = shelve.open(cache_fname)
	n_search_url = 'https://rxnav.nlm.nih.gov/REST/ndcstatus.json?ndc=' + test_ndc
	if test_ndc in cache_fobj:
		print("*** RETRIEVING data from the cached file for RXCUI ***")
		result = cache_fobj[test_ndc]
		cache_fobj.close()
		return result
	else:
		n_status = requests.get(n_search_url)
		print("*** ADDING saved data to cache file for RXCUI ***")
		cache_fobj[test_ndc] = n_status.text
		cache_fobj.close()
		return n_status.text

def get_RXCUI_info(search_results, test_ndc, rxcui_cache_fname):
	rxcui_cache_fobj = shelve.open(rxcui_cache_fname)
	status = search_results['ndcStatus']['status']
	if status == 'Alien' or status == 'Unknown':
		rxcui = (test_ndc)
		drug_name = "Unknown Drug"
	else:
		rxcui_list= search_results['ndcStatus']['ndcHistory']
		rxcui = find_active_rxcui(rxcui_list)
		if rxcui in rxcui_cache_fobj:
			print("*** RETRIEVING Rxcui from cached file! ***")
			drug_name = rxcui_cache_fobj[rxcui]
			rxcui_cache_fobj.close()
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
		rxcui_cache_fobj.close()
	return (rxcui, drug_name, status)

## set up empty lists
full_row_list= []
updated_spreadsheet = []

## Set up cache file names
cache_fname = "cached_NDC_results"
rxcui_cache_fname = "cached_RXCUI_results"
unkown_data_file = "data.txt"

with open(unkown_data_file) as json_file:
	data = json.load(json_file)

#Prompt user for filename
fname = input("Enter the CSV file you want to perform NDC lookup on: ")
try:
	ifile  = open(fname +'.csv')
except:
	print("Enter a valid CSV file name. (You do not need to include '.csv' at the end)")
	exit()

reader = csv.reader(ifile)
for row in reader:
	full_row_list.append(row)
ifile.close()

## Create the "Header Row" for each list
updated_spreadsheet.append(full_row_list[0])
updated_spreadsheet[0].append('RXCUI')
updated_spreadsheet[0].append('Drug name')
updated_spreadsheet[0].append('Hydroxyurea?')

## Generate a list on screen of all column headers
print("\n", "Column Headers:")
for each in range(len(updated_spreadsheet[0])):
	print(each+1, ":", updated_spreadsheet[0][each])

## Determine which column corresponds to NDC ##
NDC = input("Type the number of the column containing the NDC number: ")
try:
	NDC = int(NDC)-1
except:
	print("You must enter a valid number corresponding to the column!")
	exit()

count = 1
fail= 0
for ndc in full_row_list[1:]:
	test_ndc = ndc[NDC]
	if len(test_ndc) <11 and len(test_ndc) >6:
		test_ndc = test_ndc.rjust(11,'0')

	print("\nTest NDC #", count, test_ndc)
	if test_ndc in data:
		print("Retrieving Manual NDC results")
		rxcui_results = []
		rxcui_results.append("Not found in RxNorm")
		rxcui_results.append(data[test_ndc])
		rxcui_results.append("No")
	else:
		result = initial_ndc_query(test_ndc, cache_fname= cache_fname)
		search_results = json.loads(result)
		rxcui_results = get_RXCUI_info(search_results, test_ndc, rxcui_cache_fname= rxcui_cache_fname)

	ndc.append(rxcui_results[0])
	ndc.append(rxcui_results[1])
	if rxcui_results[0] in hydroxyurea_rxcui_list:
		ndc.append("Yes")
	else:
		ndc.append("No")
	updated_spreadsheet.append(ndc)
	count +=1
	if rxcui_results[1] == "Unknown Drug":
		fail +=1

match_rate = float(((count-fail)-1)/(count-1))
print("\n\nLength of updated spreadsheet: ", (len(updated_spreadsheet)-1))
print("NDC numbers without drug information found: ", fail)
print("Percent of NDC matching = ", match_rate)	

# ## Generate a new CSV file with all original data plus 
# ## 3 new columns specifying RXCUI, Drug Name and which category of antibiotic
spreadsheet_filename = fname + '_hydroxyurea_results.csv'
updated_dataframe = pd.DataFrame(updated_spreadsheet)
updated_dataframe.to_csv(spreadsheet_filename, index= False, header= False)