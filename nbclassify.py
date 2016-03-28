import json
import os
import sys
import math
pronouns=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now',]
punctuations=['!','"','#','$','%','&','\'',',','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
filewrite=open('nboutput.txt','w+')
with open('nbmodel.txt', 'r') as fp:
    data = json.load(fp)

# for key in data:
# 	print key,data[key]


for root, dirs, files in os.walk(sys.argv[1]):
	for i in range(0,len(files)):
		wordlist=[]
		#print math.log(0.25,2)
		posprob=-2
		negprob=-2
		truthprob=-2
		fakeprob=-2
		if(files[i]=='.DS_Store' or files[i]=='LICENSE' or files[i]=='README.md' or files[i]=='README.txt'):
			print " "
		else:
			filename=root+'/'+files[i]
			print filename
			f=open(filename, 'r')
			contents=f.read()
			contents=contents.lower()
			for z in range(0,len(punctuations)):
				if punctuations[z] in contents:
					#print punctuations[z]
					if punctuations[z]!='\'':
						contents=contents.replace(punctuations[z]," ")
					else:
						contents=contents.replace(punctuations[z],"")
					
			contents=contents.split()
			
			for z in range(0,len(contents)):
				if contents[z] not in pronouns:
					wordlist.append(contents[z])
			#print wordlist
			for z in range(0,len(wordlist)):
				if wordlist[z] in data:
					

					posprob=posprob+math.log(data[wordlist[z]][0],2)
					
					negprob=negprob+math.log(data[wordlist[z]][1],2)
					
					truthprob=truthprob+math.log(data[wordlist[z]][2],2)
					
					fakeprob=fakeprob+math.log(data[wordlist[z]][3],2)
				
			print posprob,negprob,truthprob,fakeprob
			#print math.pow(2,posprob),math.pow(2,negprob),math.pow(2,truthprob),math.pow(2,fakeprob)
			
			if(max(truthprob,fakeprob)==  truthprob):
				#print "truthful"
				filewrite.write("truthful ")
			else:
				filewrite.write("deceptive ")
				#print "deceptive"

			if(max(posprob,negprob)==posprob):
				#print "positive"
				filewrite.write("positive ")
			else:
				#print "negative"	
				filewrite.write("negative ")
			filewrite.write(filename+"\n")