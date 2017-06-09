'''this function helps in generating the language model input'''

import string
import sys

def createInput(inputFile,outputFile):
	punctuation = string.punctuation.replace("|","")
	data=[]
	f=open(inputFile,'r')
	for line in f:
		words = line.strip().split()
		for i in range(len(words)):
			if words[i].find("-") == -1:
				words[i] = words[i].translate(string.maketrans("",""), punctuation)
		line = ' '.join(words)
		line = line.replace("  ", " ")
		data.append(line)
	f.close()

	f=open(outputFile,'w')
	f.write('\n'.join(data))
	f.close()

def main():
	if len(sys.argv)!=3:                                                                               #check arguments
		print "Usage :: python languageModelInput trainSource.txt trainS.txt "
		sys.exit(0)

	createInput(sys.argv[1], sys.argv[2])

if __name__ == "__main__":                                                                              #main
    main()