import csv

# sort Korean participants by immersion & proficiency
# ignored orthographical errors, and missing determiners
# X means not ditransitive
# excluded 'throw at', 'pay with', 'award with' and 'throw for + infinitive clause'
# included 'award for'+IO, bring for'+IO and 'give for'+IO

# import each data item as a dictionary, store in list
with open('English_Response_Data.csv', 'rU') as fp:
	reader = csv.reader(fp)
	keys = reader.next()
	E_data = []
	print keys
	for row in reader:
		item = {}
		for i in range(len(row)):
			item[keys[i]] = row[i]
		E_data.append(item)


with open('Korean_Response_Data.csv', 'rU') as fp:
	reader = csv.reader(fp)
	keys = reader.next()
	K_data = []
	print keys
	for row in reader:
		item = {}
		for i in range(len(row)):
			item[keys[i]] = row[i]
		K_data.append(item)

# analyze data
def analyze(data):
	E_counts = {i['Verb'].strip():{'PO':0, 'DO':0} for i in E_data}
	for item in data:
		if item["Freaky"] == "" and item["DO/PO"] != "X":
			E_counts[item["Verb"]][item["DO/PO"]] += 1

	for x in E_counts.keys():
		print x, E_counts[x]

analyze(E_data)
print "_____________"
analyze(K_data)

# Look at inclusive & exclusive percentages
# Correct some corrections for difference from mean 
# calculate based on Bernolet & Haartsuiker