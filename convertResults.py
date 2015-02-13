import csv
import re

completions = []

def guessConstruction(fragment):
	if re.match(r'.+ to ((?:the)|(?:a)|(?:an)) .+', fragment) != None:
		return "PO"
	elif re.match(r'((?:the)|(?:a)|(?:an)) \S+ ((?:the)|(?:a)|(?:an)) \S+', fragment) != None:
		return "DO"
	elif re.match(r'^((?:the )|(?:a )|(?:an ))?\S+$', fragment):
		return "X"
	
	else: return None

with open('Norming_Study__English.csv', 'rU') as fp:
	reader = csv.reader(fp)
	keys = reader.next()
	beginnings = reader.next()
	for row in reader:
		# Check for Finished = 1
		if row[9] == "1":
			i = 12
			while row[i] != "-1":
				if keys[i][0] == 'd' and len(row[i]) > 1:
					completions.append([beginnings[i].split(" ")[-1], 
										beginnings[i], row[i], 
										guessConstruction(row[i])])
				i += 1

with open('English_response_data.csv', 'w') as fp:
    writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Verb', 'Beginning', 'Completion', 'DO/PO', 'Freaky'])
    for c in completions:
    	writer.writerow(c)