'''after obtaining the consistent phrases from the phrase extraction algorithm we next move to find the translationProbability
this is done by calculating the relative occurrences of the target phrase for a given source phrase for both directions'''
'''it takes as input the phrases.txt file and returns the translationProbability in the file named 
translationProbabilityTargetGivenSource.txt and translationProbabilitySourceGivenTarget.txt'''

from collections import defaultdict
import sys
import math

countTarget=defaultdict(lambda: defaultdict(int))
sumCountSource=defaultdict(int)
countSource = defaultdict(lambda: defaultdict(int))
sumCountTarget = defaultdict(int)


def findTranslationProbability(phrasesFile):

	f = open (phrasesFile, 'r')
	for line in f:
		phrases = line.strip().split('\t')
		if len(phrases) == 2:
			countTarget[phrases[0]][phrases[1]]+=1
			sumCountSource[phrases[0]]+=1
			countSource[phrases[1]][phrases[0]]+=1
			sumCountTarget[phrases[1]]+=1
	f.close

	data=[]
	for key in countTarget:
		for key1 in countTarget[key]:
			translationProbability = math.log(float(countTarget[key][key1])/sumCountSource[key])
			data.append(key1+'\t'+key +'\t'+str(translationProbability))

	f=open('translationProbabilityTargetGivenSource.txt','w')
	f.write('\n'.join(data))
	f.close()

	data=[]
	for key in countSource:
		for key1 in countSource[key]:
			translationProbability = math.log(float(countSource[key][key1])/sumCountTarget[key])
			data.append(key1+'\t'+key+'\t'+str(translationProbability))

	f=open('translationProbabilitySourceGivenTarget.txt','w')
	f.write('\n'.join(data))
	f.close()

def main():
	if len(sys.argv)!=2:                                                                               #check arguments
		print "Usage :: python findTranslationProbability phrases.txt"
		sys.exit(0)

	findTranslationProbability(sys.argv[1])

if __name__ == "__main__":                                                                              #main
    main()
