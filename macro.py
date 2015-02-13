mport csv
import numpy as np
import matplotlib.pyplot as plt

# Create data structure to fill with data from analysis
class item(name, link, frag):


# open the csv data in universal newline mode
with open('items.csv', 'rU') as csvfile:
	for row in csv.reader(csvfile):
		# Each row's item becomes an entry in dictionary with its columns as
		# the appropriate entries
		data_dict[row[0]] = {"lemma": row[1], "verb": row[2], 
							"type": row[5].strip(), "tense":row[7]}


'''[[AdvancedFormat]]			
[[ED:State]]	
[[ED:Gender]]	
[[ED:SawSurvey:1]]	
[[Block:block1]]	
[[Question: TextEntry:form]]	
[[ID:i01p1]]	
<img src='http://i60.tinypic.com/2hdvcqp.jpg' height='350'>
[[Choices]]	
<div style='text-align: right;'>The baby is </div>	
[[PageBreak]]	
[[Question: TextEntry:form]]	
[[ID:dt01p1]]	
<img src='http://i57.tinypic.com/6yz33q.jpg' height='350'>
[[Choices]]	
<div style='text-align: right;'>The man showed</div>
[[PageBreak]]	
[[Block:block2]]	
[[Question: TextEntry:form]]	
[[ID:i02p2]]	
<img src='http://i61.tinypic.com/2ebv37s.jpg' height='350'>
[[Choices]]	
<div style='text-align: right;'>The man is </div>	
[[PageBreak]]	
[[Question: TextEntry:form]]	
[[ID:dt02p1]]	
<img src='http://i60.tinypic.com/9g9b7r.jpg' height='350'>
[[Choices]]	
<div style='text-align: right;'>The boy handed</div>'''