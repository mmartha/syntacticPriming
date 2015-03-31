import csv
import re


def guessConstruction(fragment):
	# Look for sentences with "to the __" or "to a(n) __", these are likely PO
	if re.match(r'.+ to ((?:the)|(?:a)|(?:an)|(?:her)|(?:his)) .+', fragment) != None:
		return "PO"
	# Look for "the __ the __" or "a __ a __"; these are likely DO
	elif re.match(r'((?:the)|(?:a)|(?:an)|(?:her)|(?:his)) \S+ ((?:the)|(?:a)|(?:an)|(?:her)|(?:his)) \S+', fragment) != None:
		return "DO"
	# If the sentence completion contains only one object, it is not a ditransitive 
	# completion. E.g "[gave] the hat" is coded as X
	elif re.match(r'^((?:the )|(?:a )|(?:an )|(?:her )|(?:his ))?\S+$', fragment):
		return "X"
	
	else: return None


def gradePrimeCompletion(fragment, condition):
	if condition.strip() == "PO":
		# Look for sentences beginning with "to the/a/an/his/her __"
		if re.match(r'^(to ((?:the)|(?:a)|(?:an)|(?:her)|(?:his)) .+)$', fragment) != None:
			return 1
		else: return 0
	elif condition.strip() == "DO":
		# Look for "the/a/an/his/her/some __"
		if re.match(r'^(((?:the)|(?:a)|(?:an)|(?:her)|(?:his)|(?:some)) .+)$', fragment) != None:
			return 1
		else: return 0
	# other condition is neutral, any completion is acceptable
	elif condition.strip() == "neutral": return 1


# create list of experimental prime & target pairs
trials = []

# load item dictionary
items = {}
with open('items.csv', 'rU') as f:
	for row in csv.reader(f):
		items[row[1]] = {"type": row[0].strip(), "item": row[1].strip(), 
								"verb":row[2].strip(), "condition":row[4].strip()}


# parse results
with open('Syntactic_Priming_Korean_Data.csv', 'rU') as fp:
	data_rows = csv.reader(fp)
	# set keys as first line of csv file
	keys = data_rows.next()
	# set sentence beginnings as second line
	beginnings = data_rows.next()
	finished_index = beginnings.index("Finished")
	version_index = keys.index("Version")
	filler_version_index = keys.index("FillerVersion")
	

	# next row is subject 1
	subj = 1
	for subject in data_rows:
		# Check if subject finished survey
		if subject[finished_index] == "1":
			
			# iterate i until keys are picture items
			i = filler_version_index
			while (keys[i][-4:] != "TEXT"): 
				i+=1
			
			# experimental items' column labels end in TEXT
			while (keys[i][-4:] == "TEXT"):
				# We don't care about filler sentence completions or items not seen
				if keys[i][:6] != "filler" and len(subject[i])>1:
					# to get item id's from column labels we have to cut off extra junk
					try:
						cutoff_p = keys[i][:-6].index("-")
					except ValueError:
						cutoff_p = keys[i][:-6].index("_")
					try:
						cutoff_t = keys[i+1][:-6].index("-")
					except ValueError:
						cutoff_t = keys[i+1][:-6].index("_")
	
					prime_id = keys[i][:cutoff_p]
					target_id = keys[i+1][:cutoff_t]

					# get values for this trial
					prime_verb = items[prime_id]["verb"]
					prime_condition = items[prime_id]["condition"]
					prime_completion = subject[i]
					target_completion = subject[i+1]
					p_beginning = beginnings[i]
					beginning = beginnings[i+1]
					target_verb = items[target_id]["verb"]

					# append these values as a list within the trials list
					trials.append([subj, target_id, prime_verb, prime_condition,
						p_beginning, prime_completion, 
						gradePrimeCompletion(prime_completion, prime_condition),
						target_verb, beginning, 
						target_completion, guessConstruction(subject[i+1])])
					i += 2
				else: i += 1
		print ".",
		subj += 1

with open('Korean_Priming_processed_data.csv', 'w') as fp:
    writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    # Create Column labels
    writer.writerow(['Subject ID', 'Target ID', 
    				'Prime Verb', 'Prime Condition', 'Prime Beginning', 'Prime Completion', 'completion grade', 
    				'Target Verb', 'Target Beginning', 'Target Completion','DO/PO', 'Freaky'])
    for c in trials:
    	writer.writerow(c)
    print "\n File Korean_Priming_processed_data.csv has been written"



