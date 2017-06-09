#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''this function gives the translation for a given sentence based on hypothesis recombiniation.'''
'''it takes as input the finalTranslationProbability and the input file and returns the output translation in translation.txt'''

import sys
from collections import defaultdict
import operator
import string
import codecs
from nltk.translate import PhraseTable
from nltk.translate import StackDecoder

def findBestTranslation(finalTranslationProbability, inputFile):
	punctuation = string.punctuation
	punctuation = punctuation.replace("-","").replace("|","")
	tp = defaultdict(dict)
	f=open(finalTranslationProbability,'r')
	for line in f:
		line = line.strip().split('\t')
		line[0] = line[0].translate(string.maketrans("",""), punctuation)
		line[1] = line[1].translate(string.maketrans("",""), punctuation)
		tp[line[0]][line[1]] = float(line[2])
	f.close()
	
	data=[]
	f=open(inputFile,'r')

	for i, line in enumerate(f):
		translationScore = defaultdict(int)
		translationSentence = defaultdict(list)
		phrases = defaultdict(list)

		words = line.strip().split(' ')
		for i in range(len(words)):
			words[i] = words[i].translate(string.maketrans("",""), punctuation)
		count = 1
		for i in range(len(words)):
			translation = ''
			translatephrase = ''
			for j in range(len(words)-count+1):
				phrase = words[j:j+count]
				phrase = ' '.join(phrase)
				if phrase in tp:
					translationPhrase = max(tp[phrase].iteritems(), key=operator.itemgetter(1))[0]
					translationScore[count]+=tp[phrase][translationPhrase]
					translation+=translationPhrase+' '
					translatephrase += phrase+ ' '
			if translation!='':
				translationSentence[count].append(translation)
				phrases[count].append(translatephrase)
				
			count+=1

		if len(translationScore) != 0:
			index = max(translationScore.iteritems(), key=operator.itemgetter(1))[0]
			finalTranslation = ' '.join(translationSentence[index])
			finalTranslatePhrase = ' '.join(phrases[index])
			words = line.strip().split(' ')
			finalTranslationWords = finalTranslation.strip().split(' ')
			for i, word in enumerate(words):
				tmp = []
				if word not in finalTranslatePhrase:
					tmp.extend(finalTranslationWords[:i])
					tmp.append(word)
					tmp.extend(finalTranslationWords[i:])
					finalTranslationWords = tmp
			finalTranslation = ""
			for word in finalTranslationWords:
				finalTranslation += word.strip() + " "
		else:
			finalTranslation = line.strip()
		
		data.append(finalTranslation.strip().replace("  "," "))

	f = codecs.open('translation.txt',"w","utf-8")
	for line in data:
		f.write(line.decode("utf-8") + "\n")
	f.close()


def main():
	if len(sys.argv)!=3:                                                                               #check arguments
		print "Usage :: python stackDecoder.py finalTranslationProbability.txt inputFile.txt "
		sys.exit(0)

	findBestTranslation(sys.argv[1], sys.argv[2])

if __name__ == "__main__":                                                                              #main
    main()