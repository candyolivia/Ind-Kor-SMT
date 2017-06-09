import nltk
from nltk.translate.bleu_score import SmoothingFunction
from string import punctuation
import decimal

chencherry = SmoothingFunction()

def countBLEUfromSentence(ref, hyp):
	hyp = ''.join([ch for ch in hyp if ch not in punctuation])
	ref = ''.join([ch for ch in ref if ch not in punctuation])
	BLEUscore = nltk.translate.bleu_score.corpus_bleu([[ref.split()]], [hyp.split()],smoothing_function=chencherry.method4)

	return BLEUscore*100

def countBLEUfromFile(ref, hyp):
	f = open(ref)
	references = f.readlines()
	f = open(hyp)
	outputs = f.readlines()
	sum = 0
	for i in range(len(references)):
		try:
			sum += countBLEUfromSentence(references[i],outputs[i])
		except ZeroDivisionError:
			sum = sum

	avg = sum/len(references)	
	print "avg = " + str(avg)

def countBLEUfromEachSentence(ref, hyp):
	f = open(ref, "r")
	references = f.readlines()
	f = open(hyp, "r")
	hyp = f.readlines()

	f = open("eval.txt", "w")
	for i in range(len(references)):
		print i
		try:
			f.write(str(countBLEUfromSentence(references[i],hyp[i])))
		except ZeroDivisionError:
			f.write("0")
		f.write("\n")
