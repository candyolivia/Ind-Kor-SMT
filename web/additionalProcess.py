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


class Additional():
	def __init__(self):
		with open("kamus/kbbi.txt",'r') as file:
			self.kbbi = [line.rstrip("\n") for line in file]
		self.indVocab = self.getIndonesianVocab()
		self.korealemma = self.getkordictionary()
		file = open("kamus/id_reorder.txt", "r")
		lines = [line.rstrip() for line in file]
		self.idtags = []
		self.idorders = []
		for i,line in enumerate(lines):
			self.idtags.append(line.split("\t")[0])
			self.idorders.append(line.split("\t")[1])
		file = open("kamus/kr_reorder.txt", "r")
		lines = [line.rstrip() for line in file]
		self.krtags = []
		self.krorders = []
		for i,line in enumerate(lines):
			self.krtags.append(line.split("\t")[0])
			self.krorders.append(line.split("\t")[1])

	def similar(self,a,b):
	    return SequenceMatcher(None, a, b).ratio()

	def getIndonesianMorphs(self,word):
		w = Word(word, language="id")
		return w.morphemes

	def getIndonesianVocab(self):
		vocabs = []
		f = open("kamus/vocab.txt","r")
		lines = f.readlines()
		for i, line in enumerate(lines):
			if self.isAlpha(line.split(" ")[1]):
				vocabs.append(line.split(" ")[1])
		return vocabs

	def addPOSTAGIndonesia(self,string):
		out = sentence_extraction(cleaning(string))

		if len(out) <= 1 and len(out[0].split(" ")) <= 1:
			result = out[0] + '|NN'
		else:
			for o in out:
				strtag = " ".join(tokenisasi_kalimat(o)).strip()
				result = " ".join(mt.taggingStr(strtag))

		result = result.replace("/","|")
		return result

	def addLemma(self,string):
		newSentence = ""
		words = string.split(" ")
		for word in words:
			newSentence = newSentence + word + "|" + stemmer.stem(word) + " "
		result = newSentence.strip()
		return result

	def isAlpha(self,word):
		return str.isalpha(word)

	def cleankordictionary(self,word):
		brackets = re.findall('\[.*?\]',word)
		for bracket in brackets:
			word = word.replace(bracket, "")
		brackets = re.findall('\(.*?\)',word)
		for bracket in brackets:
			word = word.replace(bracket, "")
		return word

	def getkordictionary(self):
		file = open("kamus/KamusKorea.csv","r")
		lines = file.readlines()
		kordictionary = []
		f = codecs.open("kamus/test.txt","w","utf-8")
		for line in lines:
			ind = [self.cleankordictionary(x).strip() for x in line.split("\t")[0].split(",")]
			kor = [self.cleankordictionary(x).strip() for x in line.split("\t")[1].split(",")]
			if not (len(ind) == 1 and ind[0] == ""):
				if not (len(kor) == 1 and kor[0] == ""):
					dic = {}
					dic["id"] = ind
					dic["kr"] = kor
					string = ", ".join(ind)
					string += "\t"
					string += ", ".join(kor)
					string = string.replace("~","")
					f.write(unicode(self.cleankordictionary(string),"utf-8") + "\n")
					ind = [self.cleankordictionary(x).strip() for x in string.split("\t")[0].split(",")]
					kor = [self.cleankordictionary(x).strip() for x in string.split("\t")[1].split(",")]
					kordictionary.append(dic)
		return kordictionary

	def translateIndToKr(self,word):
		for kordictionary in self.korealemma:
			for indo in kordictionary["id"]:
				if word == indo:
					return kordictionary["kr"][0]

	def translateKrToInd(self,word):
		for kordictionary in self.korealemma:
			if type(kordictionary["kr"][0]) == type(word) and kordictionary["kr"][0] == word:
				return kordictionary["id"][0]
			else:
				if type(kordictionary["kr"][0]) != type(word):
					if (kordictionary["kr"][0] == word.encode("utf-8")):
						return kordictionary["id"][0]

		for kordictionary in self.korealemma:
			if len(kordictionary["kr"]) > 1:
				if type(kordictionary["kr"][1]) == type(word) and word == kordictionary["kr"][1]:
					return kordictionary["id"][0]
				else:
					if type(kordictionary["kr"][1]) != type(word):
						if word.encode("utf-8") == kordictionary["kr"][1]:
							return kordictionary["id"][0]

		for kordictionary in self.korealemma:
			if len(kordictionary["kr"]) > 2:
				if type(kordictionary["kr"][2]) == type(word) and word == kordictionary["kr"][2]:
					return kordictionary["id"][0]
				else:
					if type(kordictionary["kr"][2]) != type(word):
						if word.encode("utf-8") == kordictionary["kr"][2]:
							return kordictionary["id"][0]

	def findAlphabet(self,sentence):
		words = sentence.split(" ")
		for i in range(len(words)):
			if words[i].isalnum():
				return i

	def is_hangul(self,ch):
	    if ch is None:
	        return False
	    else:
			return ord(ch) >= 0xac00 and ord(ch) <= 0xd7a3

	def findHangul(self,sentence):
		words = sentence.split(" ")
		for i in range(len(words)):
			# print words[i]
			if not words[i][0].isalnum() and not words[i][0] in string.punctuation:
				return i

	def translateIndNgram(self,string,n,start):
		string += " "
		words = string.split(" ")
		while len(words) > n and start < (len(words)-n):
			words = string.split(" ")
			ngram = ""
			for i in range(n):
				ngram += words[i+start] + " "
			if ngram.strip() != "":
				if self.translateIndToKr(ngram.strip()) is not None:
					string = string.replace(ngram, self.translateIndToKr(ngram.strip()).decode("utf-8")+" ")
					start += n
				else:
					start += 1
			else:
				start += 1
		return string.replace("~","")

	def translateKorNgram(self,string,n,start):
		string += " "
		words = string.split(" ")
		print words
		while len(words) > n and start < (len(words)-n):
			words = string.split(" ")
			ngram = ""
			for i in range(n):
				ngram += words[i+start] + " "
			if ngram.strip() != "":
				if self.translateKrToInd(ngram.strip()) is not None:
					string = string.replace(ngram, self.translateKrToInd(ngram.strip())+" ")
					start += n
				else:
					start += 1
			else:
				start += 1
		return string.replace("~","")

	def translateIndLemma(self,string):
		string += " "
		words = string.split(" ")
		start = self.findAlphabet(string)
		if start is not None:
			while len(words) > 1 and start < (len(words)-1):
				if words[start].strip() != "" and self.isAlpha(words[start]):
					if self.translateIndToKr(stemmer.stem(words[start])) is not None:
						string = string.replace(words[start], self.translateIndToKr(stemmer.stem(words[start]))+" ")
				start += 1
		return string.replace("~","")

	def addPOSTAGKorea(self,string):
		newSentence = ""
		unicodeString = unicode(string, "utf-8")
		tagged_words = mecab.pos(unicodeString)
		for w, t in tagged_words:
			newSentence = newSentence + w + "|" + t + " "
		result = newSentence.strip()
		return result

	def postTranslate(self,mode,sentence):
		# mode = 0 (ID-KR), mode = 1 (KR-ID)
		if mode == 0:
			start = self.findAlphabet(sentence)
			if start is not None:
				for i in reversed(range(3)):
					sentence = self.translateIndNgram(sentence,i,start)
			return self.translateIndLemma(sentence.encode("utf-8"))
		elif mode == 1:
			sentence = self.deleteParticle(sentence).encode("utf-8")
			start = self.findHangul(sentence)
			if start is not None:
				for i in reversed(range(3)):
					sentence = self.translateKorNgram(sentence,i,start)
			print sentence
			return self.transAddKRVerb(sentence).encode("utf-8")

	def deleteParticle(self,sentence):
		particle = ["JKB","JX","JKS","JKO","JKG","XSN"]
		postaggedSentence = self.addPOSTAGKorea(sentence)
		units = postaggedSentence.split(" ")
		result = ""
		for unit in units:
			postag = unit.split("|")[1]
			if postag not in particle:
				result += " " + unit.split("|")[0]
		return result.strip()

	def transAddKRVerb(self,sentence):
		tags = ["VA","VA","VV"]
		postaggedSentence = self.addPOSTAGKorea(sentence)
		units = postaggedSentence.split(" ")
		result = ""
		for unit in units:
			postag = unit.split("|")[1]
			if postag in tags:
				if self.translateKrToInd(unit.split("|")[0] + u"다") is not None:
					result += " " + self.translateKrToInd(unit.split("|")[0] + u"다")
				else:
					result += " " + unit.split("|")[0]
			else:
				result += " " + unit.split("|")[0]
		return result.strip()

	def transIndNE(self,sentence):
		tags = ["NNP","NN"]
		exception = ["ku", "mu", "nya"]
		postaggedSentence = self.addPOSTAGIndonesia(sentence)
		units = postaggedSentence.split(" ")
		result = ""
		for unit in units:
			postag = unit.split("|")[1]
			if postag == "NNP" and unit.split("|")[0].strip() not in exception:
				result += " " + self.hangulizeRoman(unit.split("|")[0])
			elif postag == "NN" and unit.split("|")[0].strip() not in exception and stemmer.stem(unit.split("|")[0]) not in self.kbbi:
				result += " " + self.hangulizeRoman(unit.split("|")[0])
			else:
				result += " " + unicode(unit.split("|")[0],"utf-8")
		return result.strip()

	def transKorNE(self,sentence):
		tags = ["NNP","NNG"]
		postaggedSentence = self.addPOSTAGKorea(sentence.strip())
		units = postaggedSentence.split(" ")
		result = ""
		for unit in units:
			postag = unit.split("|")[1]
			if postag in tags:
				string = unit.split("|")[0].encode("utf-8")
				score = 0
				temp = unit.split("|")[0].encode("utf-8")
				for vocab in self.indVocab:
					if score < self.similar(vocab, self.romanizeHangul(string)):
						score = self.similar(vocab, self.romanizeHangul(string))
						temp = vocab
				if score > 0.8:
					result += " " + temp
				else:
					result += " " + self.romanizeHangul(string)
			else:
				result += " " + unit.split("|")[0]
		return result.strip()

	def hangulizeRoman(self,string):
		return hangulize(string.decode("utf-8"),"ron")

	def romanizeHangul(self,string):
		return transliter.translit(string.decode("utf-8")).replace("-","")

	def postProcessIndNE(filename):
		file = open(filename, 'r')
		newFilename = filename.replace(filename.split("/")[-1],"") + "nameentity/" + filename.split("/")[-1]
		output = codecs.open(newFilename,'w', "utf-8")

		lines = file.readlines()
		for i, line in enumerate(lines):
			print i
			if self.findAlphabet(line) is not None:
				output.write(self.transIndNE(line.strip()) + "\n")
			else:
				output.write(unicode(line.strip(),"utf-8") + "\n")

	def countParticle(self,filename):
		file = open(filename, 'r')
		output = open("err1.txt",'w')
		particle = ["JKS","JKC","JKG","JKO","JKB","JKV","JKQ","JC","JX"]

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

	def postProcessKorNE(self,filename):
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

	def postProcess(self,mode,filename):
		file = open(filename, 'r')
		newFilename = filename.replace(filename.split("/")[-1],"") + "verb/" + filename.split("/")[-1]
		output = codecs.open(newFilename,'w', "utf-8")

		lines = file.readlines()
		for i, line in enumerate(lines):
			print i
			if line.strip() == "":
				output.write(unicode(line.strip(),"utf-8") + "\n")
			elif self.findHangul(line.strip()) is not None:
				output.write(self.postTranslate(mode,line.strip()).decode("utf-8") + "\n")
			else:
				output.write(unicode(line.strip(),"utf-8") + "\n")

	def getOnlyPostagID(self,sentence):
		postaggedSentence = self.addPOSTAGIndonesia(sentence).replace("aku|NN","aku|PRP").replace("kapan|NN","kapan|WP")
		words = postaggedSentence.split(" ")
		tags = ""
		for word in words:
			postag = word.split("|")[1]
			tags += postag + " "
		return tags.strip()

	def getOnlyPostagKR(self,sentence):
		postaggedSentence = self.addPOSTAGKorea(sentence).replace("aku|NN","aku|PRP").replace("kapan|NN","kapan|WP")
		words = postaggedSentence.split(" ")
		tags = ""
		for word in words:
			postag = word.split("|")[1]
			tags += postag + " "
		return tags.strip()

	def reorderIndonesia(self,sentence):
		words = sentence.split(" ")
		postag = self.getOnlyPostagID(sentence.strip())
		order = "-1"
		if postag in self.idtags:
			order = self.idorders[self.idtags.index(postag)]

			for i in range(len(words)):
				order = order.replace(" " + str(i+1) + " ", " " + words[i]+ " ")
		else:
			order = sentence.strip()
		return order

	def reorderKorea(self,sentence):
		words = sentence.strip().split(" ")
		postag = self.getOnlyPostagKR(sentence.strip())
		order = "-1"
		print postag
		if postag in self.krtags:
			order = self.krorders[self.krtags.index(postag)]

			for i in range(len(words)):
				order = order.replace(" " + str(i+1) + " ", " " + words[i]+ " ")
		else:
			order = sentence.strip()
		return order

	def reversePhrase(self,string):
		phrases = string.split("%")
		phrases = list(reversed(phrases))
		result = ""
		for phrase in phrases:
			result += phrase + " "
		return result.strip()

	def translateReorderedIDKR(self,inp,reorderedSentence):
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
					if len(trans.split("%")) > 1:
						result += self.reversePhrase(trans) + " "
					else:
						result += trans.strip() + " "
		return result

	def translateReorderedKRID(self,inp,reorderedSentence):
		t = Translator()
		phrases =  re.findall("\((.*?)\)", reorderedSentence)
		result = ""
		if len(t.translateKRID(inp).split("%")) <= 1:
			result = t.translateKRID(inp).strip()
		else:
			if reorderedSentence.find("(") == -1:
				result = t.translateKRID(reorderedSentence).strip()
			else:
				for phrase in phrases:
					trans = t.translateKRID(phrase)
					if len(trans.split("%")) > 1:
						result += self.reversePhrase(trans) + " "
					else:
						result += trans.strip() + " "
		return result
