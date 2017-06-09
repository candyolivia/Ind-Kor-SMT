#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from polyglot.text import Text, Word
import codecs
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys 
import os, re
from hanja import hangul
from nltk.tokenize.util import is_cjk
from konlpy.tag import Mecab
from hangulize import hangulize
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
from translate import Translator

sys.path.append(os.path.abspath(os.getcwd() + "/pebahasa"))

import suku
from hmmtagger import MainTagger
from tokenization import *
from capschunking import *
from difflib import SequenceMatcher

mecab = Mecab()
factory = StemmerFactory()
stemmer = factory.create_stemmer()
mt = MainTagger("pebahasa/resource/Lexicon.trn", "pebahasa/resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)
transliter = Transliter(academic)

with open("kbbi.txt",'r') as file:
	kbbi = [line.rstrip("\n") for line in file]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getIndonesianMorphs(word):
	w = Word(word, language="id")
	return w.morphemes

def getIndonesianVocab():
	vocabs = []
	f = open("vocab.txt","r")
	lines = f.readlines()
	for i, line in enumerate(lines):
		if isAlpha(line.split(" ")[1]):
			vocabs.append(line.split(" ")[1])
	return vocabs

def addPOSTAGIndonesia(string):
	out = sentence_extraction(cleaning(string))

	if len(out) <= 1 and len(out[0].split(" ")) <= 1:
		result = out[0] + '|NN'
	else:
		for o in out:
			strtag = " ".join(tokenisasi_kalimat(o)).strip()
			result = " ".join(mt.taggingStr(strtag))
	
	result = result.replace("/","|")
	return result

def addLemma(string):
	newSentence = ""
	words = string.split(" ")
	for word in words:
		newSentence = newSentence + word + "|" + stemmer.stem(word) + " "
	result = newSentence.strip()
	return result

def isAlpha(word):
	return str.isalpha(word)

def cleankordictionary(word):
	brackets = re.findall('\[.*?\]',word)
	for bracket in brackets:
		word = word.replace(bracket, "")
	brackets = re.findall('\(.*?\)',word)
	for bracket in brackets:
		word = word.replace(bracket, "")
	return word

def getkordictionary():
	file = open("kamus/KamusKorea.csv","r")
	lines = file.readlines()
	kordictionary = []
	f = codecs.open("kamus/test.txt","w","utf-8")
	for line in lines:
		ind = [cleankordictionary(x).strip() for x in line.split("\t")[0].split(",")]
		kor = [cleankordictionary(x).strip() for x in line.split("\t")[1].split(",")]
		if not (len(ind) == 1 and ind[0] == ""):
			if not (len(kor) == 1 and kor[0] == ""):
				dic = {}
				dic["id"] = ind
				dic["kr"] = kor
				string = ", ".join(ind)
				string += "\t"
				string += ", ".join(kor)
				string = string.replace("~","")
				f.write(unicode(cleankordictionary(string),"utf-8") + "\n")
				ind = [cleankordictionary(x).strip() for x in string.split("\t")[0].split(",")]
				kor = [cleankordictionary(x).strip() for x in string.split("\t")[1].split(",")]
		
				kordictionary.append(dic)
	return kordictionary

korealemma = getkordictionary()

def translateIndToKr(word):
	for kordictionary in korealemma:
		for indo in kordictionary["id"]:
			if word == indo:
				return kordictionary["kr"][0]

def translateKrToInd(word):
	for kordictionary in korealemma:
		if type(kordictionary["kr"][0]) == type(word) and kordictionary["kr"][0] == word:
			return kordictionary["id"][0]
		else:
			if type(kordictionary["kr"][0]) != type(word):
				if (kordictionary["kr"][0] == word.encode("utf-8")):
					return kordictionary["id"][0]		
				
	for kordictionary in korealemma:
		if len(kordictionary["kr"]) > 1:
			if type(kordictionary["kr"][1]) == type(word) and word == kordictionary["kr"][1]:
				return kordictionary["id"][0]
			else:
				if type(kordictionary["kr"][1]) != type(word):
					if word.encode("utf-8") == kordictionary["kr"][1]:
						return kordictionary["id"][0]
	
	for kordictionary in korealemma:
		if len(kordictionary["kr"]) > 2:
			if type(kordictionary["kr"][2]) == type(word) and word == kordictionary["kr"][2]:
				return kordictionary["id"][0]
			else:
				if type(kordictionary["kr"][2]) != type(word):
					if word.encode("utf-8") == kordictionary["kr"][2]:
						return kordictionary["id"][0]

def findAlphabet(sentence):
	words = sentence.split(" ")
	for i in range(len(words)):
		if words[i].isalnum():
			return i

def is_hangul(ch):
    if ch is None:
        return False
    else:
		return ord(ch) >= 0xac00 and ord(ch) <= 0xd7a3

def findHangul(sentence):
	words = sentence.split(" ")
	for i in range(len(words)):
		# print words[i]
		if not words[i][0].isalnum() and not words[i][0] in string.punctuation:
			return i

def translateIndNgram(string, n,start):
	string += " "
	words = string.split(" ")
	while len(words) > n and start < (len(words)-n):
		words = string.split(" ")
		ngram = ""
		for i in range(n):
			ngram += words[i+start] + " "
		if ngram.strip() != "":
			if translateIndToKr(ngram.strip()) is not None:
				string = string.replace(ngram, translateIndToKr(ngram.strip())+" ")
				start += n
			else:
				start += 1
		else:
			start += 1
	return string.replace("~","")

def translateKorNgram(string, n,start):
	string += " "
	words = string.split(" ")
	while len(words) > n and start < (len(words)-n):
		words = string.split(" ")
		ngram = ""
		for i in range(n):
			ngram += words[i+start] + " "
		if ngram.strip() != "":
			if translateKrToInd(ngram.strip()) is not None:
				string = string.replace(ngram, translateKrToInd(ngram.strip())+" ")
				start += n
			else:
				start += 1
		else:
			start += 1
	return string.replace("~","")

def translateIndLemma(string):
	string += " "
	words = string.split(" ")
	start = findAlphabet(string)
	if start is not None:
		while len(words) > 1 and start < (len(words)-1):
			if words[start].strip() != "" and isAlpha(words[start]):
				if translateIndToKr(stemmer.stem(words[start])) is not None:
					string = string.replace(words[start], translateIndToKr(stemmer.stem(words[start]))+" ")
			start += 1
	return string.replace("~","")

def addPOSTAGKorea(string):
	newSentence = ""
	unicodeString = unicode(string, "utf-8")
	tagged_words = mecab.pos(unicodeString)
	for w, t in tagged_words:
		newSentence = newSentence + w + "|" + t + " "
	result = newSentence.strip()
	return result

def postTranslate(mode, sentence):
	# mode = 0 (ID-KR), mode = 1 (KR-ID)
	# print sentence
	if mode == 0:
		start = findAlphabet(sentence)
		if start is not None:
			for i in reversed(range(3)):
				sentence = translateIndNgram(sentence,i,start)

		return translateIndLemma(sentence)
		# return sentence
	elif mode == 1:
		# sentence = deleteParticle(sentence).encode("utf-8")
		start = findHangul(sentence)
		if start is not None:
			for i in reversed(range(3)):
				sentence = translateKorNgram(sentence,i,start)
		# return transAddKRVerb(deleteParticle(sentence).encode("utf-8")).encode("utf-8")
		return transAddKRVerb(sentence).encode("utf-8")
		# return deleteParticle(sentence).encode("utf-8")
		# return sentence

def deleteParticle(sentence):
	particle = ["JKB","JX","JKS","JKO","JKG"]
	postaggedSentence = addPOSTAGKorea(sentence)
	units = postaggedSentence.split(" ")
	result = ""
	for unit in units:
		postag = unit.split("|")[1]
		if postag not in particle:
			result += " " + unit.split("|")[0]
	return result.strip()

def transAddKRVerb(sentence):
	tags = ["VA","VA","VV"]
	postaggedSentence = addPOSTAGKorea(sentence)
	units = postaggedSentence.split(" ")
	result = ""
	for unit in units:
		postag = unit.split("|")[1]
		if postag in tags:
			if translateKrToInd(unit.split("|")[0] + u"다") is not None:
				result += " " + translateKrToInd(unit.split("|")[0] + u"다")
			else:
				result += " " + unit.split("|")[0]
		else:
			result += " " + unit.split("|")[0]
	return result.strip()

def transIndNE(sentence):
	tags = ["NNP","NN"]
	exception = ["ku", "mu", "nya"]
	postaggedSentence = addPOSTAGIndonesia(sentence)
	# print postaggedSentence
	units = postaggedSentence.split(" ")
	result = ""
	for unit in units:
		postag = unit.split("|")[1]
		# if postag in tags:
		if postag == "NNP" and unit.split("|")[0].strip() not in exception:
			result += " " + hangulizeRoman(unit.split("|")[0])
		elif postag == "NN" and unit.split("|")[0].strip() not in exception and stemmer.stem(unit.split("|")[0]) not in kbbi:
			result += " " + hangulizeRoman(unit.split("|")[0])
		# else:
		# 	result += " " + unit.split("|")[0]

		else:
			result += " " + unicode(unit.split("|")[0],"utf-8")
	
	return result.strip()


indVocab = getIndonesianVocab()

def transKorNE(sentence):
	tags = ["NNP"]
	postaggedSentence = addPOSTAGKorea(sentence.strip())
	units = postaggedSentence.split(" ")
	result = ""
	for unit in units:
		postag = unit.split("|")[1]
		if postag in tags:
			string = unit.split("|")[0].encode("utf-8")
			score = 0
			temp = unit.split("|")[0].encode("utf-8")
			for vocab in indVocab:
				if score < similar(vocab, romanizeHangul(string)):
					score = similar(vocab, romanizeHangul(string))
					temp = vocab
			# print romanizeHangul(string)
			
			if score > 0.8:
				result += " " + temp
			else:
				result += " " + romanizeHangul(string)
		else:
			result += " " + unit.split("|")[0]
	return result.strip()

def hangulizeRoman(string):
	return hangulize(string.decode("utf-8"),"ron")

def romanizeHangul(string):
	return transliter.translit(string.decode("utf-8")).replace("-","")

def postProcessNE(filename):
	file = open(filename, 'r')
	newFilename = filename.replace(filename.split("/")[-1],"") + "nameentity/" + filename.split("/")[-1]
	output = codecs.open(newFilename,'w', "utf-8")
	# output2 = codecs.open(newFilename2,'w', "utf-8")

	lines = file.readlines()
	for i, line in enumerate(lines):
		print i
		if findAlphabet(line) is not None:
			output.write(transIndNE(line.strip()) + "\n")
		else:
			output.write(unicode(line.strip(),"utf-8") + "\n")

def containNotTranslatedInd(filename):
	file = open(filename, 'r')
	output = open("ind_err1.txt",'w')
	
	lines = file.readlines()
	for i, line in enumerate(lines):
		print i
		splitLine = line.split(" ")
		count = 0
		for word in splitLine:
			if findAlphabet(word) is not None:
				count += 1
		output.write(str(count) + "/" + str(len(splitLine)) + "\n")


def countParticle(filename):
	file = open(filename, 'r')
	output = open("err1.txt",'w')
	particle = ["JKB","JX","JKS","JKO","JKG"]
	
	lines = file.readlines()
	for i, line in enumerate(lines):
		print i
		postaggedSentence = addPOSTAGKorea(line.strip())

		splitLine = postaggedSentence.split(" ")
		count = 0
		for word in splitLine:
			if word.split("|")[1] in particle:
				count += 1
		output.write(str(count) + "\n")


def postProcessNE2(filename):
	file = open(filename, 'r')
	newFilename = filename.replace(filename.split("/")[-1],"") + "nameentity/" + filename.split("/")[-1]
	output = codecs.open(newFilename,'w', "utf-8")

	lines = file.readlines()
	for i, line in enumerate(lines):
		print i
		if findHangul(line.strip()) is not None:
			output.write(transKorNE(line.strip()) + "\n")
		else:
			output.write(unicode(line.strip(),"utf-8") + "\n")

def containNotTranslatedKor(filename):
	file = open(filename, 'r')
	output = open("kor_err1.txt",'w')
	lines = file.readlines()
	for i, line in enumerate(lines):
		print i
		splitLine = line.strip().split(" ")
		count = 0
		for word in splitLine:
			if findHangul(word.strip()) is not None:
				count += 1
		output.write(str(count) + "/" + str(len(splitLine)) + "\n")


def postProcess(mode,filename):
	file = open(filename, 'r')
	newFilename = filename.replace(filename.split("/")[-1],"") + "verb/" + filename.split("/")[-1]
	output = codecs.open(newFilename,'w', "utf-8")

	lines = file.readlines()
	for i, line in enumerate(lines):
		print i
		if line.strip() == "":
			output.write(unicode(line.strip(),"utf-8") + "\n")
		elif findHangul(line.strip()) is not None:
			output.write(postTranslate(mode,line.strip()).decode("utf-8") + "\n")
		else:
			output.write(unicode(line.strip(),"utf-8") + "\n")

file = open("id_reorder.txt", "r")
lines = [line.rstrip() for line in file]
idtags = []
idorders = []
for i,line in enumerate(lines):
	idtags.append(line.split("\t")[0])
	idorders.append(line.split("\t")[1])

def getOnlyPostagID(sentence):
	postaggedSentence = addPOSTAGIndonesia(sentence).replace("aku|NN","aku|PRP").replace("kapan|NN","kapan|WP")
	words = postaggedSentence.split(" ")
	tags = ""
	for word in words:
		postag = word.split("|")[1]
		tags += postag + " "
	return tags.strip()

def getOnlyPostagKR(sentence):
	postaggedSentence = addPOSTAGKorea(sentence).replace("aku|NN","aku|PRP").replace("kapan|NN","kapan|WP")
	words = postaggedSentence.split(" ")
	tags = ""
	for word in words:
		postag = word.split("|")[1]
		tags += postag + " "
	return tags.strip()

def reorderIndonesia(sentence):
	words = sentence.split(" ")
	postag = getOnlyPostagID(sentence.strip())
	order = "-1"
	# print postag
	if postag in idtags:
		order = idorders[idtags.index(postag)]

		for i in range(len(words)):
			order = order.replace(" " + str(i+1) + " ", " " + words[i]+ " ")
	else:
		order = sentence.strip()
	# print order
	return order

def reorderKorea(sentence):
	words = sentence.strip().split(" ")
	postag = getOnlyPostagKR(sentence.strip())
	order = "-1"
	# print postag
	if postag in idtags:
		order = idorders[idtags.index(postag)]

		for i in range(len(words)):
			order = order.replace(" " + str(i+1) + " ", " " + words[i]+ " ")
	else:
		order = sentence.strip()
	# print order
	return order

def reversePhrase(string):
	phrases = string.split("%")
	phrases = list(reversed(phrases))
	result = ""
	for phrase in phrases:
		result += phrase + " "
	return result.strip()

def translateReordered(inp, reorderedSentence):
	t = Translator()
	phrases =  re.findall("\((.*?)\)", reorderedSentence)
	result = ""
	if len(t.translateIDKR(inp).split("%")) <= 1:
		result = t.translateIDKR(inp).strip()
	else:
		if reorderedSentence.find("(") == -1:
			result = t.translateIDKR(reorderedSentence).strip()
		else:
			for phrase in phrases:
				trans = t.translateIDKR(phrase)
				# trans = t.translateKRID(phrase)

				# print t.translateIDKR("dan")
				# trans = translateIndNgram(phrase,3,0)
				# trans = translateIndLemma(phrase)
				if len(trans.split("%")) > 1:
					result += reversePhrase(trans) + " "
				else:
					result += trans.strip() + " "
			print inp, result
	return result

# file = open("final/reorder/bukuS.txt","r")
# file2 = open("final/reorder/bukuT.txt","r")
# lines2 = file2.readlines()
# lines = file.readlines()
# f = codecs.open("final/reorder/buku/bukuIndonesiaTranslation.txt","w","utf-8")
# for i,line in enumerate(lines):
# 	data = reorderIndonesia(line)
# 	print i, lines2[i].strip()
# 	# try:
# 	translateReordered(line,data).replace("  ", "").replace("%","")
# 	# except Exception, e:
# 	# 	translateReordered(line,data).replace("  ", "").decode("utf-8").replace("%","")+"\n"