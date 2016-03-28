import sys
import os
import re
import json
pronouns=['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now',]
punctuations=['!','"','#','$','%','&','\'',',','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']

wordDict={}
uniqueSet=set()
def getTempList(temp):
	global posCount,negCount,truthCount,fakeCount
	if(posFlag==1):
		temp['pos']+=1
	if(negFlag==1):
		temp['neg']+=1
		
	if(truthfulFlag==1):
		temp['truth']+=1
		
	if(fakeFlag==1):
		temp['fake']+=1
		
	return temp

def getEmptyList():
	temp={'pos':0,'neg':0,'truth':0,'fake':0}
	
	return temp
probDict={}
def getFeatures():
	for key in wordDict:
		tempList=[]
		temp=wordDict[key]
		tempList.append((temp['pos']+1)/float(posCount+len(uniqueSet)))
		tempList.append((temp['neg']+1)/float(negCount+len(uniqueSet)))
		tempList.append((temp['truth']+1)/float(truthCount+len(uniqueSet)))
		tempList.append((temp['fake']+1)/float(fakeCount+len(uniqueSet)))
		probDict[key]=tempList


posCount=0
posFiles=0
negCount=0
negFiles=0
truthCount=0
truthFiles=0
fakeCount=0
fakeFiles=0
for root, dirs, files in os.walk(sys.argv[1]):
	

	for i in range(0,len(files)):
		negFlag=0
		posFlag=0
		fakeFlag=0
		truthfulFlag=0
		wordlist=[]
		if(files[i]=='.DS_Store' or files[i]=='LICENSE' or files[i]=='README.md' or files[i]=='README.txt'):
			print " "
		else:
			filename=root+'/'+files[i]
			#print filename
			f=open(filename, 'r')
			contents=f.read()
			contents=contents.lower()
			#print contents

			for z in range(0,len(punctuations)):
				if punctuations[z] in contents:
					#print punctuations[z]
					if punctuations[z]!='\'':
						contents=contents.replace(punctuations[z]," ")
					else:
						contents=contents.replace(punctuations[z],"")
					
			contents=contents.split()
			#print contents
			for z in range(0,len(contents)):
				if contents[z] not in pronouns:
					wordlist.append(contents[z])
			
			if(re.search( r'(.)*positive_polarity(.)*', root)):
				posFlag=1
				posCount+=len(wordlist)
				posFiles+=1
				if(re.search( r'(.)*truthful(.)*', root)):
					truthfulFlag=1
					truthCount+=len(wordlist)
					truthFiles+=1
				elif(re.search( r'(.)*deceptive(.)*', root)):
					fakeFlag=1
					fakeCount+=len(wordlist)
					fakeFiles+=1
			elif(re.search( r'(.)*negative_polarity(.)*', root)):
				negFlag=1
				negCount+=len(wordlist)
				negFiles+=1
				if(re.search( r'(.)*truthful(.)*', root)):
					truthfulFlag=1
					truthCount+=len(wordlist)
					truthFiles+=1
				elif(re.search( r'(.)*deceptive(.)*', root)):
					fakeFlag=1
					fakeCount+=len(wordlist)
					fakeFiles+=1

			#print posFlag,negFlag,fakeFlag,truthfulFlag
			#print wordlist
			temp={}
			for z in range(0,len(wordlist)):
				uniqueSet.add(wordlist[z])
				if wordlist[z] in wordDict:
					temp=wordDict[wordlist[z]]
					temp=getTempList(temp)
					wordDict[wordlist[z]]=temp
				else:
					temp=getEmptyList()
					temp=getTempList(temp)
					wordDict[wordlist[z]]=temp
	#raw_input()


#print wordDict
# for key in wordDict:
# 	print key,wordDict[key]
#print posCount,negCount,truthCount,fakeCount
#print posFiles,negFiles,truthFiles,fakeFiles
#print len(uniqueSet)

#print posCount,negCount,truthCount,fakeCount

getFeatures()
# for key in probDict:
# 	print key,probDict[key]
with open('nbmodel.txt', 'w+') as fp:
    json.dump(probDict, fp)

    
