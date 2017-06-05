import requests
import json

rxcui_dictionary = {}

run = True
while run == True:
	search_term = input("What drug name would you like? (or type 'done' to move on to the next section) ")
	if search_term.lower() == "done":
		run = False
	else:
		search_url = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + search_term
		response = requests.get(search_url)
		resp = json.loads(response.text)
		try:
			rxnormId = resp['idGroup']['rxnormId']
			count = 1
		except:
			print("no drug name found for that search, check spelling")
			continue
		for each in range(len(rxnormId)):
			# current_rxnormId = rxnormId[each]
			# rxcui_dictionary[current_rxnormId]= {}
			rxcui_lookup_url = "https://rxnav.nlm.nih.gov/REST/rxcui/" + str(rxnormId[each]) + "/related.json?tty=BPCK+GPCK+SBD+SCD"
			print(rxcui_lookup_url)
			rxcui_response = requests.get(rxcui_lookup_url)
			rxcui_resp = json.loads(rxcui_response.text)
			print(count, "rxcui RESPONSE: ", rxcui_resp)
			count +=1
			# print("1st level", rxcui_resp['relatedGroup'].keys())
			# print("2nd level", rxcui_resp['relatedGroup']['conceptGroup'])
			for each in rxcui_resp['relatedGroup']['conceptGroup']:
				if (len(each)) <=1:
					pass
				else:
					for drug in each['conceptProperties']:
						print("rxcui: ", drug['rxcui'])
						print("name: ", drug['name'])
						rxcui = drug['rxcui']
						name = drug['name']
						rxcui_dictionary[rxcui]= name
			print("output:", rxcui_dictionary)


## which ones does the user want to keep?
## run through them one by one to 
for key, value in rxcui_dictionary.items():
	print("RXCUI: ", key, "Drug Name: ", value, "\n")
	answer = 0
	while answer == 0:
		answer = input("Do you wish to keep this drug in your target list? Y or N?   ")
		if answer.lower() == "y":
			break
		elif answer.lower() == "n":
			rxcui_dictionary[key] = 0
			break
		else:
			print("\n You didn't select Y or N!\n")
			continue

### how to force an answer???


drugs_to_remove = [key for key, value in rxcui_dictionary.items()
                  if value == 0]
for key in drugs_to_remove:
    del rxcui_dictionary[key]
print("final dictionary", rxcui_dictionary)