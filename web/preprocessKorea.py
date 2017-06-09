#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from konlpy.tag import Mecab
from konlpy.tag import Twitter
from konlpy.utils import pprint
import hanja
import codecs
import string

mecab = Mecab()
twitter = Twitter()

def splitSentenceToMorphsMecab(string):
	newSentence = ""
	unicodeString = unicode(string, "utf-8")
	morphs = mecab.morphs(unicodeString)
	for morph in morphs:
		newSentence = newSentence + " " + morph
	result = unicode(newSentence.strip())
	return result

def splitSentenceToMorphsTwitter(string):
	newSentence = ""
	unicodeString = unicode(string, "utf-8")
	morphs = twitter.morphs(unicodeString)
	for morph in morphs:
		newSentence = newSentence + " " + morph
	result = unicode(newSentence.strip())
	return result

def preprocessKoreanCorpus(filename):
	file = open(filename, 'r')
	newFilename = "new_" + filename
	newFilename = filename
	output = codecs.open(newFilename.replace(".","")+".txt",'w', "utf-8")
	lines = file.readlines()
	for line in lines:
		output.write(splitSentenceToMorphsMecab(line) + "\n")

def addPOSTAG(string):
	newSentence = ""
	unicodeString = unicode(string, "utf-8")
	tagged_words = mecab.pos(unicodeString)
	for w, t in tagged_words:
		newSentence = newSentence + w + "|" + t + " "
	result = newSentence.strip()
	return result

def is_hangul(ch):
    if ch is None:
        return False
    else:
		return ord(ch) >= 0xac00 and ord(ch) <= 0xd7a3

def addIsHangul(string):
	newSentence = ""
	morphs = string.split(" ")
	for morph in morphs:
		newSentence = newSentence + morph + "|" + str(is_hangul(unicode(morph[0]))) + " "
	result = newSentence.strip()
	return result

def preprocessKoreanWithPOStag(filename):
	file = open(filename, 'r')
	newFilename = filename
	output = codecs.open(newFilename.replace(".","")+".txt",'w', "utf-8")
	lines = file.readlines()
	for line in lines:
		output.write(addPOSTAG(line) + "\n")