'''-t'''
''' it takes as input the word alignment of both the languages and returns a file called phrases.txt which contains
all the consistent phrases'''

import sys                                                                                             #import libraries
from alignment import findAlignment

def checkConsistency(fstart, fend, estart, eend, wordAlignment, source, target):
	'''function to check whether the phrase is consistent or not'''
	flag =1

	listSource =[]
	listTarget = []

	for i in range(len(source)):
		if i >= estart and i<=eend:
			listSource.append(i)

	for i in range(len(target)):
		if i >= fstart and i <=fend:
			listTarget.append(i)

	for e in listSource:
		for f in range(len(target)):
			if wordAlignment[e][f]==1:
				if f >= fstart and f <=fend:
					continue
				else:
					flag = 0

	for f in listTarget:
		for e in range(len(source)):
			if wordAlignment[e][f]==1:
				if e >= estart and e <=eend:
					continue
				else:
					flag = 0

	return flag


def findPhrase(fstart, fend, estart, eend, source, target):
	'''given the starting and end points, it returns the phrase for both the source and the target language'''
	phraseE = []
	#print fstart, fend, estart, eend
	for i in range(estart,eend+1):
		phraseE.append(source[i])

	phraseG = []
	for i in range(fstart,fend+1):
		try:
			phraseG.append(target[i])
		except IndexError:
			break
		

	return [' '.join(phraseE), ' '.join(phraseG)]

def extract(fstart, fend, estart, eend, wordAlignment, source, target):
	'''this method extracts the consistent phrases and returns it to the extractPhrases method'''
	if fend == -1:
		return 'NULL'

	else:
		flag=checkConsistency(fstart, fend, estart, eend, wordAlignment, source, target)
		if flag:
			return findPhrase(fstart, fend, estart, eend, source, target)
		else:
			return 'NULL'

def extractPhrases(sourceToTarget, targetToSource):
	'''this method reads the file for both the source and target language and returns the phrases extracted from the
	sentences. The phrases are consistent in nature'''

	data=[]
	feg = open(sourceToTarget, 'r')
	fge = open(targetToSource,'r')
	count = 0
	while True:
		count+=1
		print count
		line = feg.readline()
		if line == "":
			break
		sourceToTarget1 = feg.readline()
		sourceToTarget2 = feg.readline()
		#print sourceToTarget1
		line = fge.readline()
		targetToSource1 = fge.readline()
		targetToSource2 = fge.readline()
		#print targetToSource1

		wordAlignment, source, target = findAlignment(sourceToTarget1, sourceToTarget2, targetToSource1, targetToSource2)

		lSource = len(source)
		lTarget = len(target)
		
		phrases = []
		for estart in range(lSource):
			for eend in range(estart,(lSource)):
				fstart = lTarget
				fend = -1
				for i in wordAlignment:
					if i <= eend and i >= estart:
						for j in wordAlignment[i]:
							fstart = min(j, fstart)
							fend = max(j, fend)
				if ((eend - estart) <= 20) or ((fend -fstart) <= 20) :
					phrases.append([estart, eend, fstart, fend])
		# print phrases
		for key in phrases:
			estart = key[0]
			eend = key[1]
			fstart = key [2]
			fend = key[3]
			phrase = extract (fstart, fend,estart, eend,wordAlignment, source, target)
			if phrase!= 'NULL':
				#print phrase
				tmp = (phrase[0].strip()+'\t'+phrase[1].strip())
				if tmp.strip()!= "" and tmp not in data:
					data.append(tmp)
	feg.close()
	fge.close()

	f=open('phrases.txt','w')
	f.write('\n'.join(data))
	f.close()
	
def main():
	if len(sys.argv)!=3:                                                                               #check arguments
		print "Usage :: python phraseExtraction.py sourceToTarget targetToSource"
		sys.exit(0)

	extractPhrases(sys.argv[1], sys.argv[2])

if __name__ == "__main__":                                                                              #main
    main()
