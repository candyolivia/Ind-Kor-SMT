#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, re
from collections import defaultdict
import operator
import string
import codecs
from nltk.translate import PhraseTable
from nltk.translate import StackDecoder
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
from preprocessIndonesian import splitPossessiveWords
from preprocessKorea import splitSentenceToMorphsMecab

class Translator():
	def preprocessID(self, string):
		string = string.lower().replace('\'','').replace('"','').replace(':','')
		line = re.sub('([.,!?():;/])', r' \1 ', string)
		line = re.sub('\s{2,}', ' ', line)
		words = line.split(" ")
		for i in range(len(words)):
			if words[i].strip()[-1:] == "-":
				words[i] = words[i][:-1]
		line = " ".join(words)
		return splitPossessiveWords(line)

	def preprocessKR(self, string):
		string = string.lower().replace('\'','').replace('"','').replace(':','')
		line = re.sub('([.,!?():;/])', r' \1 ', string)
		line = re.sub('\s{2,}', ' ', line)
		words = line.split(" ")
		for i in range(len(words)):
			if words[i].strip()[-1:] == "-":
				words[i] = words[i][:-1]
		line = " ".join(words)
		return splitSentenceToMorphsMecab(line)

	def translateIDKR(self, input):
		finalTranslationProbability = "../final/baseline/bukusubtitle/finalTranslationProbabilitySourceGivenTarget.txt"
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

		translationScore = defaultdict(int)
		translationSentence = defaultdict(list)
		phrases = defaultdict(list)

		words = input.strip().split(' ')
		for i in range(len(words)):
			words[i] = str(words[i]).translate(string.maketrans("",""), punctuation)
		count = 1
		for i in range(len(words)):
			translation = ''
			translatephrase = ''
			for j in range(len(words)-count+1):
				phrase = words[j:j+count]
				phrase = ' '.join(phrase)
				#print phrase
				if phrase in tp:
					translationPhrase = max(tp[phrase].iteritems(), key=operator.itemgetter(1))[0]
					translationScore[count]+=tp[phrase][translationPhrase]
					translation+= translationPhrase +'%% '
					# translation+= translationPhrase +' '
					translatephrase += phrase+ ' '
			if translation!='':
				translationSentence[count].append(translation)
				phrases[count].append(translatephrase)
				
			count+=1

		if len(translationScore) != 0:
			index = max(translationScore.iteritems(), key=operator.itemgetter(1))[0]
			finalTranslation = ' '.join(translationSentence[index])
			# finalTranslation = finalTranslation.decode("utf-8")
			finalTranslatePhrase = ' '.join(phrases[index])
			# words = line.strip().encode("utf-8").split(' ')
			words = input.strip().split(' ')
			finalTranslationWords = finalTranslation.strip().split('% ')
			for i, word in enumerate(words):
				tmp = []
				if word not in finalTranslatePhrase:
					tmp.extend(finalTranslationWords[:i])
					# tmp.append(word + "%")
					tmp.append(word + "%")
					tmp.extend(finalTranslationWords[i:])
					# print tmp
					finalTranslationWords = tmp
					# finalTranslation += " " + word
			finalTranslation = ""
			for word in finalTranslationWords:
				finalTranslation += word.decode("utf-8").strip() + " "
		else:
			finalTranslation = input.strip()
		
		data.append(finalTranslation.strip().replace("  "," "))

		# f = codecs.open('translation.txt',"w","utf-8")
		# # f = open('translation.txt',"w")
		# for line in data:
		# 	# print line
		# 	f.write(line.decode("utf-8") + "\n")
		# f.close()

		return finalTranslation.strip().replace("  "," ").replace("%%","%")

	def translateKRID(self, input):
		finalTranslationProbability = "../final/baseline/bukusubtitle/finalTranslationProbabilityTargetGivenSource.txt"
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

		translationScore = defaultdict(int)
		translationSentence = defaultdict(list)
		phrases = defaultdict(list)

		words = input.strip().split(' ')
		for i in range(len(words)):
			words[i] = str(words[i]).translate(string.maketrans("",""), punctuation)
		count = 1
		for i in range(len(words)):
			translation = ''
			translatephrase = ''
			for j in range(len(words)-count+1):
				phrase = words[j:j+count]
				phrase = ' '.join(phrase)
				#print phrase
				if phrase in tp:
					translationPhrase = max(tp[phrase].iteritems(), key=operator.itemgetter(1))[0]
					translationScore[count]+=tp[phrase][translationPhrase]
					translation+=translationPhrase+'%% '
					translatephrase += phrase+ ' '
			if translation!='':
				translationSentence[count].append(translation)
				phrases[count].append(translatephrase)
				
			count+=1

		if len(translationScore) != 0:
			index = max(translationScore.iteritems(), key=operator.itemgetter(1))[0]
			finalTranslation = ' '.join(translationSentence[index])
			# finalTranslation = finalTranslation.decode("utf-8")
			finalTranslatePhrase = ' '.join(phrases[index])
			# words = line.strip().encode("utf-8").split(' ')
			words = input.strip().split(' ')
			finalTranslationWords = finalTranslation.strip().decode("utf-8").split('% ')
			for i, word in enumerate(words):
				tmp = []
				if word not in finalTranslatePhrase:
					tmp.extend(finalTranslationWords[:i])
					tmp.append(word + "%")
					tmp.extend(finalTranslationWords[i:])
					# print tmp
					finalTranslationWords = tmp
					# finalTranslation += " " + word
			finalTranslation = ""
			for word in finalTranslationWords:
				finalTranslation += word.decode("utf-8").strip() + " "
		else:
			finalTranslation = input.strip().decode("utf-8")
		
		data.append(finalTranslation.strip().replace("  "," "))

		return finalTranslation.strip().replace("  "," ").replace("%%","%")
	
	def romanizeHangul(self, string):
		transliter = Transliter(academic)
		return transliter.translit(string.decode("utf-8")).replace("-","")
