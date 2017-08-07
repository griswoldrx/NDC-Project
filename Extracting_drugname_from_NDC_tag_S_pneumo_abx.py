import csv 
import pandas as pd 
import requests 
import json 
import pickle 
# from datetime import datetime

PCN_rxcui_list = [834046, 834040, 834061, 834102, 1088677]

Ery_rxcui_list = [197650, 686418, 903958, 903954, 425351, 245242, 313968, 206073,
310154, 206075, 310155, 598006, 245240, 206078, 848119, 315090, 597193, 206080,
848121, 310157, 197650, 487129, 486960, 486955, 597194, 486912, 686350,
863603, 686402, 686400, 863606, 686405, 686420, 686418, 750839, 686355,
750841, 686406]

Amox_rxcui_list = [1360635, 791942, 791939, 246282, 308177, 1359005, 846994, 403945,
308181, 1359009, 791944, 392151, 313797, 598025, 308182, 313850, 308188, 
1358974, 392152, 1360637, 791949, 791947, 897052, 205730, 239191, 94406, 308191,
308192, 105152, 828246, 802550, 308189, 213339, 308194]

Other_oral_abx_rxcui_list = [861689, 617995, 618028, 617993, 562253, 617309, 1810270,
617333, 617302, 824186, 562251, 617304, 1810273, 617423, 617316, 617293, 1810268,
617339, 897048, 617322, 824190, 617296, 617430, 617996, 824194, 562508, 226633,
756252, 313799, 250463, 313800, 308210, 308212, 861417, 861416, 211307, 308459, 141962,
212446, 308460, 583482, 577378, 577162, 105260, 141963, 226827, 248656, 211511, 204844,
750157, 749780, 750149, 749783, 1148107, 308985, 309041, 309043, 476322, 476325, 309044,
476327, 309045, 309040, 476623, 313888, 197449, 309042, 213828, 105171, 213839, 309047,
105170, 801153, 213840, 309048, 213823, 309049, 309054, 213199, 200346, 476576, 847365,
351127, 847362, 847360, 1043025, 1043022, 1373016, 1373014, 1043027, 581574, 309058,
1043031, 1043030, 197450, 705008, 419849, 1372999, 409823, 213927, 197451, 309079, 892782,
309076, 309077, 892784, 214078, 309078, 250156, 309080, 206288, 197452, 309081, 206298,
197453, 581580, 309087, 897288, 309085, 108395, 309086, 105189, 309095, 581583, 309096,
211974, 309097, 581584, 313926, 211979, 309098, 755615, 406696, 1312438, 1312431, 755616,
541056, 309110, 212306, 309112, 309115, 1312442, 1312440, 1867697, 759721, 645617, 755617,
309113, 212339, 309114, 197454, 1312446, 1312444, 637175, 637173, 309121, 197455, 313889,
197456, 1232977, 1232971, 197463, 1673949, 252338, 1673951, 252671, 685543, 359385, 597455,
240741, 205863, 197516, 205860, 309322, 205866, 197517, 835342, 835341, 748743, 562266,
629319, 748746, 197518, 900388, 433773, 993242, 853019, 900393, 900391, 1371353, 1085918,
1486880, 1547998, 900428, 1432125, 900424, 748748, 284215, 629324, 748750, 309329, 900462,
900460, 392275, 309372, 197533, 197534, 313945, 309860, 197595, 197596, 309956, 597521,
702296, 310026, 1650032, 597520, 1666542, 205621, 1649990, 352172, 830605, 1650142, 730065,
728207, 602175, 1650444, 861061, 1650030, 1666098, 205619, 1649401, 351997, 1652673,
1666545, 700410, 700408, 404592, 1649429, 901401, 901399, 205606, 348869, 434018, 1101055,
205604, 1649988, 1650143, 1801140, 1801138, 800493, 799048, 1543953, 1650446, 746686,
310028, 762390, 351988, 283535, 1423082, 1423080, 1653435, 1653433, 1798276, 1101019,
1649405, 1806948, 1652674, 1801144, 1801142, 352080, 348870, 406524, 1791507, 1791505,
1543955, 1649425, 835701, 835700, 795852, 757460, 795853, 757464, 795712, 757466,
686383, 310445, 644541, 314009, 637562, 637560, 200104, 200394, 200395, 544445, 477391,
211815, 199884, 211816, 199885, 284481, 311296, 755473, 756123, 311342, 311370, 197898,
311371, 197899, 1362042, 1014018, 1013659, 1302669, 858064, 858062, 1302676, 1302674,
629695, 1302656, 1302650, 629697, 1014022, 1013662, 858374, 858372, 1302659, 1014024,
1013665, 1302666, 1302664, 629699, 351974, 351121, 242807, 207355, 207356, 197984,
404094, 207364, 207352, 207353, 197985, 762420, 583282, 207362, 262221, 1486191, 314108,
404528, 403840, 198054, 312129, 198055, 105230, 317570, 542379, 312190, 1421163, 1114477,
1114473, 199997, 1549233, 142118, 208406, 313134, 208416, 198334, 198231, 246252, 849580,
198335, 1540868, 1540862, 602855, 597761, 539741, 388510, 198249, 756192, 313251, 203970,
198250, 313252, 1541233, 198252, 313254, 902644, 902640, 1094352, 261353, 562707, 108449,
198332, 198333, 199332, 581614, 311345, 314079, 262091, 311347, 197511, 197512, 199370, 
205769, 205770, 205771, 213224, 213226, 309308, 309309, 309310, 359383, 403921, 672912,
847488, 899122, 198048, 198049, 198050, 207208, 207209, 207210, 877486, 261339, 311787,
794246, 761979, 895384, 731566, 731564, 745560, 1549551, 1549546, 1484873, 1484757,
1438129, 1438136, 1438127, 731541, 731538, 836307, 836306, 731568, 745309, 731567, 745462,
731571, 731570, 207390, 204466, 207391, 617857, 617881, 312270, 105078, 995906, 863538,
745286, 745292, 745302, 1432525, 1856552, 1233294, 623695, 623677, 731575, 731572, 745477,
1090041, 1050111, 1050115, 1094911, 882546, 1233540, 1731729, 745303, 745561, 205843,
240984, 789980, 1659595, 1659592, 1721475, 308207, 105134, 1659600, 1659598, 1721476,
1721473, 1044196, 313819, 1666111, 308210, 1721474, 197389, 313855, 1668240, 1668238,
309050, 239194, 1665050, 313920, 1665060, 1665052, 1665091, 1665095, 1665093, 1665088,
1665097, 1665099, 239195, 309059, 309061, 315023, 309062, 309063, 1747117, 1747115, 1747123,
1747121, 1656316, 1656313, 105174, 309065, 1656320, 1656318, 543682, 309068, 1731542, 1722919,
1722916, 1743557, 1722921, 1739890, 1665105, 1665102, 309072, 1665109, 1665107, 1040005,
1659292, 1659294, 206422, 206423, 240447, 242800, 249926, 1659287, 1659283, 389025, 389026,
1659285, 1659289, 1659281, 1659278, 1603845, 1603840, 105183, 105184, 206554, 206559, 309088,
317075, 342957, 342958, 342959, 1597620, 1597615, 1665023, 1665005, 309090, 1665021, 309092,
1665046, 1665008, 1665447, 212075, 245239, 1665444, 309101, 1665449, 1665451, 242787, 309117,
313899, 896746, 896750, 896848, 896851, 617295, 199693, 199694, 199928, 239200, 706461, 205964,
685574, 685576, 685578, 309335, 309336, 309339, 1737578, 1737244, 1737581, 1737579, 1737245,
1737582, 1539243, 1539248, 404652, 403920, 744812, 744808, 1039654, 1039657, 310027, 544840,
1734686, 1734683, 1668267, 1668264, 259311, 284394, 1726207, 1726204, 1726216, 1726214, 1665508,
1665507, 1665516, 1665515, 1665517, 1665519, 1665504, 1665497, 1309312, 672156, 672154, 1540030,
102787, 656858, 239212, 1662280, 1662278, 1662284, 1662283, 1662286, 1662285, 1722941, 1722939,
1722937, 1722934, 311689, 207358, 317127, 860777, 351156, 239189, 1721458, 1721460, 1547620,
1547615, 312128, 240637, 312127, 1743547, 1743549, 1012989, 1012991, 312183, 1812273, 1094907,
631403, 1607973, 1812268, 248390, 1013679, 1013702, 584292, 312188, 1857717, 1047476, 1047472,
884254, 312447, 239186, 1659134, 1659131, 1659139, 1659137, 208180, 312444, 1659151, 1659149,
261306, 259290, 1809083, 313137, 1728089, 1728087, 1728085, 1728082, 853066, 351239, 313401,
313402, 313404, 584201, 581531, 1807511, 1807510, 1807508, 208812, 239209, 1807513, 313572,
1807516, 1807518]

def find_active_rxcui(ndc_history_list):
	potential_rxcui_list = []
	for each in ndc_history_list:
		potential_rxcui_list.append(each['activeRxcui'])
	l = [int(x) for x in potential_rxcui_list if x != '']
	try:
		return l[0]
	except:
		return "No Active Rxcui for this NDC"

def initial_ndc_query(test_ndc, cache_diction, cache_fname):
		n_search_url = 'https://rxnav.nlm.nih.gov/REST/ndcstatus.json?ndc=' + test_ndc
		if test_ndc in cache_diction:
			print("*** RETRIEVING data from the cached file for RXCUI ***")
			return cache_diction[test_ndc]
		else:
			n_status = requests.get(n_search_url)
			print("*** ADDING saved data to cache file for RXCUI ***")
			cache_diction[test_ndc] = n_status.text
			fobj = open(cache_fname, "wb")
			pickle.dump(cache_diction, fobj)
			fobj.close()
			return n_status.text

def get_RXCUI_info(search_results, test_ndc, rxcui_cache_diction, rxcui_cache_fname):
	status = search_results['ndcStatus']['status']
	if status == 'Alien' or status == 'Unknown':
		rxcui = (test_ndc)
		drug_name = "Unknown Drug"
		# return (rxcui, drug_name, status)
	else:
		rxcui_list= search_results['ndcStatus']['ndcHistory']
		rxcui = find_active_rxcui(rxcui_list)
		if rxcui in rxcui_cache_diction:
			print("*** RETRIEVING Rxcui from cached file! ***")
			return (rxcui, rxcui_cache_diction[rxcui], status)
		p_search_url = 'https://rxnav.nlm.nih.gov/REST/rxcui/' + str(rxcui)+ '/properties.json'
		p_properties = requests.get(p_search_url)
		RXCUI_properties = json.loads(p_properties.text)
		try:
			drug_name =RXCUI_properties['properties']['name']
		except:
			drug_name = "Unknown Drug"
		print("*** ADDING Rxcui to cached file. ***")
		rxcui_cache_diction[rxcui] = drug_name
		fobj = open(rxcui_cache_fname, "wb")
		pickle.dump(rxcui_cache_diction, fobj)
		fobj.close()

	return (rxcui, drug_name, status)

## set up empty lists
full_row_list= []
updated_spreadsheet = []

## Check for cached results file
cache_fname = "cached_NDC_results.txt"
try:
    fobj = open(cache_fname, 'rb')
    saved_cache = pickle.load(fobj)
    fobj.close()
except:
    saved_cache = {}

rxcui_cache_fname = "cached_RXCUI_results.txt"
try:
	fobj = open(rxcui_cache_fname, 'rb')
	rxcui_saved_cache = pickle.loab(fobj)
	fobj.close()
except:
	rxcui_saved_cache = {}

unkown_data_file = "data.txt"

## open and load the information from the text file into a python dictionary (JSON object) to be used for matching
## 'unknown' or 'alien' NDC numbers
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
updated_spreadsheet[0].append('Antibiotic Category')

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
		rxcui = "Not in RxNorm, manual match"
		drug_name = data[test_ndc]
		status = "Not in RxNorm"
		rxcui_results = (rxcui, drug_name, status)
	else:
		result = initial_ndc_query(test_ndc, cache_diction= saved_cache, cache_fname= cache_fname)
		search_results = json.loads(result)
		rxcui_results = get_RXCUI_info(search_results, test_ndc, rxcui_cache_diction= rxcui_saved_cache, rxcui_cache_fname= rxcui_cache_fname)

	ndc.append(rxcui_results[0])
	ndc.append(rxcui_results[1])
	if rxcui_results[0] in PCN_rxcui_list:
		ndc.append("PCN")
	elif rxcui_results[0] in Amox_rxcui_list:
		ndc.append("Amox")
	elif rxcui_results[0] in Ery_rxcui_list:
		ndc.append("Erythromycin")
	elif rxcui_results[0] in Other_oral_abx_rxcui_list:
		ndc.append("Category 4")
	else:
		ndc.append("None")

	updated_spreadsheet.append(ndc)
	count +=1
	if rxcui_results[1] == "Unknown Drug":
		fail +=1

match_rate = float(((count-fail)-1)/(count-1))
print("\n\nLength of updated spreadsheet: ", (len(updated_spreadsheet)-1))
print("NDC numbers without drug information found: ", fail)
print("Percent of NDC matching = ", match_rate)	

print("PCN", len(PCN_rxcui_list))
print("Amox", len(Amox_rxcui_list))
print("Ery", len(Ery_rxcui_list))
print("Cat 4", len(Other_oral_abx_rxcui_list))
# ## Generate a new CSV file with all original data plus 
# ## 3 new columns specifying RXCUI, Drug Name and which category of antibiotic
spreadsheet_filename = fname + 'results.csv'
updated_dataframe = pd.DataFrame(updated_spreadsheet)
updated_dataframe.to_csv(spreadsheet_filename, index= False, header= False)