'''given a pair of sentences along with the word alignment this code returns the union of the word alignment matrix'''
'''it serves as a helper function to phraseExtraction Algorithm'''

from collections import defaultdict
import string

def findAlignment(target, sourceALigned, source, targetAligned):
	punctuation = string.punctuation
	punctuation = punctuation.replace("-","").replace("|","")
	wordAlignment = defaultdict(lambda: defaultdict(int))				
	wordIndexSource = defaultdict(lambda: -1)
	wordIndexTarget = defaultdict(lambda: -1)

	target  = target.strip().split()
	for i in range(len(target)):
		target[i] = target[i].translate(string.maketrans("",""), punctuation)
		
		
	source = source.strip().split()
	for i in range(len(source)):
		source[i] = source[i].translate(string.maketrans("",""), punctuation)


	sourceALigned = sourceALigned.strip().split(" })")
	sourceALigned = sourceALigned[1:]
	count = 0
	for key in sourceALigned:
		words = key.split('({')
		if len(words)>1 and words[1]!='':
			sourceWord = words[0].strip()
			sourceWord = sourceWord.translate(string.maketrans("",""), punctuation)
			indices = words[1].split()
			for i in indices:
				i = int(i)
				wordAlignment[count][i-1] = 1
		count += 1
				
	targetAligned = targetAligned.strip().split(" })")
	targetAligned = targetAligned[1:]
	count = 0
	for key in targetAligned:
		words = key.split('({')
		if len(words)>1 and words[1]!='':
			targetWord = words[0].strip()
			targetWord = targetWord.translate(string.maketrans("",""), punctuation)
			indices = words[1].split()
			for i in indices:
				i= int(i)
				wordAlignment[i-1][count] = 1			
		count +=1

	return wordAlignment, source, target
