import csv
from random import shuffle, randint

'''
This Python script was created by Martha Hinrichs in 2014
Use this script to create a text file to be imported to Qualtrics.
The resulting script will create blocks in the following format:

	[[Block:Block_Name]]
	[[Question:TextEntry:form]]
	<<first filler item>>

	[[PageBreak]]
	[[Question:TextEntry:form]]
	<<prime item>>

	[[PageBreak]]
	[[Question:TextEntry:form]]
	<<target item>>

Blocks should then be moved around on Qualtrics in the Survey Flow.
'''

'''Set desired parameters for your survey here:'''
def main():
	versions = 3
	# blocks per version of survey
	blocks = 27 
	# total filler items
	fillers = 46 
	# max number of fillers between target trials
	max_count = 3
	# Number of different filler versions we want:
	filler_versions = 3

	create_script(versions, blocks, fillers, max_count)


def create_script(versions, blocks, fillers, max_count, filler_versions):
	# Data structure to fill with information from excel
	items = {}
	# open the csv data in universal newline mode
	with open('items.csv', 'rU') as csvfile:
		for row in csv.reader(csvfile):
			# Each sentence becomes an entry in the 'items' dictionary, with unique 
			# IDs as the keys, and dictionaries as the values (like a JSON file)
			# In this case the keys are the block names (e.g. give1D), and the data 
			# we care about are in the 2nd, 4th and 7th columns (addresses 1, 3, 6)
			# optional custom picture size variable in column 7
			items[row[1]] = {"type": row[0].strip(), "pic_url": row[3].strip(), 
								"frag":row[6].strip(), "height":row[7].strip()}

	# Ordered list which will specify the order for blocks
	order = []
	with open('blocks.csv', 'rU') as format:
		# The blocks.csv document contains the desired order of the blocks, 
		# referenced by their unique IDs
		for row in csv.reader(format):
			order.append(row)

	# Final string to be printed to text file when finished
	mystring = "[[AdvancedFormat]]\n[[ED:State]]\n[[ED:Gender]]\n[[ED:SawSurvey:1]]\n"

	# Create different versions 
	for i in range(filler_versions):
		fillerList = get_fillers(blocks, fillers, max_count)
		# for each filler version, create a list of blocks 1_1-27, 2_1-27, 3_1-27
		for j in range(len(order)):
			block = order[j]
			# x is the number 1-27, will be repeated <versions> number of times
			x = j%(len(order)/versions)
			# First item in list 'block' is block name
			mystring += "[[Block:%s]]\n" %block[0]
			# Add filler items before prime and target questions
			for k in fillerList[x]:
				mystring += "[[Question:TextEntry:form]]\n[[ID:%s]]\n<img src=\"%s\" height=\"%s\">\n[[Choices]]\n<div style=\"text-align:right;\">%s</div>\n\n[[PageBreak]]\n"% (k, items[k]["pic_url"], items[k]["height"], items[k]["frag"])
			# The rest of the items 'l' in block are question items to add to this block
			for l in block[1:]:
				if len(l) > 0:
					mystring += "[[Question:TextEntry:form]]\n[[ID:%s]]\n<img src=\"%s\" height=\"%s\">\n[[Choices]]\n<div style=\"text-align:right;\">%s</div>\n\n[[PageBreak]]\n"% (l, items[l]["pic_url"], items[l]["height"], items[l]["frag"])

	# Finally, write 'buffered' string to final document to be uploaded to Qualtrics
	with open('qualtrics.txt', 'w') as fp:
		fp.write(mystring)
		print "success"


def get_fillers(my_blocks, my_fillers, max_count):
	# Create a list of randomized filler items
	rand_filler_list = []
	temp = []
	# Create string names corresponding to filler names 
	# In this case, "filler1", "filler2", etc.
	for i in range(1,my_fillers+1):
		temp.append("filler"+str(i))
	# randomize order of filler items
	shuffle(temp)
	rand_filler_list.extend([[x] for x in temp[0:my_blocks]])
	# add remaining items randomly for varying number of fillers between blocks
	for f in temp[my_blocks:]:
		index = randint(0,my_blocks-1)
		# Prevent any block from having more than 'max_count' fillers
		while len(rand_filler_list[index]) >= max_count:
			index = randint(0, my_blocks-1)
		rand_filler_list[index].append(f)
	return rand_filler_list


if __name__ == '__main__':
    main()
