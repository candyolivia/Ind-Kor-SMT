#!/usr/bin/env python
# -*- coding: utf-8 -*-

from polyglot.text import Text, Word
import codecs
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys
import os

sys.path.append(os.path.abspath(os.getcwd() + "/pebahasa"))

import suku
from hmmtagger import MainTagger
from tokenization import *
from capschunking import *

factory = StemmerFactory()
stemmer = factory.create_stemmer()
mt = MainTagger("pebahasa/resource/Lexicon.trn", "pebahasa/resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)

with open("kamus/kbbi.txt",'r') as file:
	kbbi = [line.rstrip("\n").lower() for line in file]

def getIndonesianMorphs(word):
	w = Word(word, language="id")
	return w.morphemes

def splitPossessiveWordsKBBI(string, dictionary):
	postfix = ["mu", "ku", "nya"]
	words = string.split(" ")
	newSentence = ""
	for word in words:
		if len(word) > 3:
			if (word[:-2].lower() in dictionary) & ((word[-2:] == postfix[0]) | (word[-2:] == postfix[1])):
				word = word[:-2] + " " + word[-2:]
			elif (word[:-3].lower() in dictionary) & (word[-3:] == postfix[2]):
				word = word[:-3] + " " + word[-3:]
		newSentence = newSentence + " " + word

	return newSentence.strip()

def splitPossessiveWords(string):
	postfix = ["mu", "ku", "nya"]
	prefix = ["ku", "kau"]
	exception = ["bertanya-tanya"]
	words = string.split(" ")
	newSentence = ""
	for word in words:
		if len(word) > 4 and word not in kbbi and word not in exception:
			if stemmer.stem(word) in kbbi:
				word2 = word.replace(stemmer.stem(word),"-"+stemmer.stem(word)+"-")
				morphs = word2.split("-")
				# print morphs
				morphs2 = getIndonesianMorphs(word)
				if morphs2[-1] in postfix: # kepunyaan
					word = ""
					for i in range(0,len(morphs2)-1):
						word = word + morphs2[i]
					if word[-1:] == "-":
						word = word[:-1]
					word = word + " " + morphs2[-1]
				elif morphs[-1] in postfix: # kepunyaan
					word = ""
					for i in range(0,len(morphs)-1):
						word = word + morphs[i]
					word = word + " " + morphs[-1]
				elif morphs[0] in prefix: # subjek
					word = ""
					for i in range(1,len(morphs)):
						word = word + morphs[i]
					word = morphs[0] + " " + word

		newSentence = newSentence + " " + word

	return newSentence.strip()

def preprocessIndonesianCorpus(filename):
	file = open(filename, 'r')
	newFilename = filename
	output = open(newFilename.replace(".","")+".txt",'w')
	lines = file.readlines()
	for line in lines:
		output.write(splitPossessiveWords(line.lower()) + "\n")

def preprocessIndonesianCorpusAddPostag(filename):
	file = open(filename, 'r')
	newFilename = filename
	output = open(newFilename.replace(".","")+".txt",'w')
	lines = file.readlines()
	for i,line in enumerate(lines):
		print i
		output.write(addPOSTAG(splitPossessiveWords(line.lower())) + "\n")

def addPOSTAG(string):
	out = sentence_extraction(cleaning(string))
	for o in out:
		strtag = " ".join(tokenisasi_kalimat(o)).strip()
		result = " ".join(mt.taggingStr(strtag))
	if string != "":
		result = result.replace("/","|")
	else:
		result = ""
	return result

def addLemma(string):
	newSentence = ""
	words = string.split(" ")
	for word in words:
		newSentence = newSentence + word + "|" + stemmer.stem(word) + " "
	result = newSentence.strip()
	return result
