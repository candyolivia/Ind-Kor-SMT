from calculateBLEU import countBLEUfromSentence
from calculateBLEU import countBLEUfromFile
from preprocessKorea import preprocessKoreanCorpus
from preprocessIndonesian import preprocessIndonesianCorpus
from phraseExtraction import extractPhrases

def splitData(filename, n):
	ext = filename.split(".")[1]
	file = open(filename, "r")
	lines = file.readlines()
	iteration = 1

	testing = open("final/postag/all/test." + ext, "w")
	training = open("final/postag/all/train." + ext, "w")
	tmp = []
	for i in range(len(lines)/n):
		print i*n+iteration
		testing.write(lines[i*n+iteration])
		tmp.append(i*n+iteration)

	for i in range(len(lines)):
		if i not in tmp:
			training.write(lines[i])

def splitData2(filename, n):
	ext = filename.split(".")[1]
	file = open(filename, "r")
	lines = file.readlines()
	iteration = 1

	testing = open("test/additional/test." + ext, "w")
	training = open("test/additional/train." + ext, "w")
	tmp = []
	for i in range(len(lines)/n):
		print i*n+iteration
		testing.write(lines[i*n+iteration])
		tmp.append(i*n+iteration)

	for i in range(len(lines)):
		if i not in tmp:
			training.write(lines[i])

def preprocess(indonesia, korea):
	preprocessKoreanCorpus(korea)
	preprocessIndonesianCorpus(indonesia)

source = "corpus/subtitle.id"
target = "corpus/subtitle.kr"
# source = "final/postag/all/testS.txt"
# target = "final/postag/all/testT.txt"
# splitData(source,21)
# splitData(target,21)
# preprocess("final/postag/all/train.id","final/postag/all/train.kr")
# preprocess("final/postag/all/test.id","final/postag/all/test.kr")
# preprocessIndonesianCorpus("final/postag/all/test.id")

# run splitData 1-N validation
# preprocess pl the data
# # Run GIZA++ to build alignment model
# cd ../boost_1_55_0/mosesdecoder/giza-pp/GIZA++
# ./plain2snt.out ../../../../ind-kr-smt/final/postag/all/trainid.txt ../../../../ind-kr-smt/final/postag/all/trainkr.txt
# ./plain2snt.out ../../../../ind-kr-smt/final/postag/all/testid.txt ../../../../ind-kr-smt/final/postag/all/testkr.txt
# ./snt2cooc.out ../../../../ind-kr-smt/final/postag/all/trainid.vcb ../../../../ind-kr-smt/final/postag/all/trainkr.vcb ../../../../ind-kr-smt/final/postag/all/trainid_trainkr.snt > cooc.cooc
# ./GIZA++ -s ../../../../ind-kr-smt/final/postag/all/trainid.vcb -t ../../../../ind-kr-smt/final/postag/all/trainkr.vcb -c ../../../../ind-kr-smt/final/postag/all/trainid_trainkr.snt -CoocurrenceFile cooc.cooc
# move and rename the A3.final/postag file to sourceAlignment.txt
# ./plain2snt.out ../../../../ind-kr-smt/final/postag/all/trainkr.txt ../../../../ind-kr-smt/final/postag/all/trainid.txt
# ./snt2cooc.out ../../../../ind-kr-smt/final/postag/all/trainkr.vcb ../../../../ind-kr-smt/final/postag/all/trainid.vcb ../../../../ind-kr-smt/final/postag/all/trainkr_trainid.snt > cooc.cooc
# ./GIZA++ -s ../../../../ind-kr-smt/final/postag/all/trainkr.vcb -t ../../../../ind-kr-smt/final/postag/all/trainid.vcb -c ../../../../ind-kr-smt/final/postag/all/trainkr_trainid.snt -CoocurrenceFile cooc.cooc
# move and rename the A3.final/postag file to targetAlignment.txt
# cd ../../../../ind-kr-smt
# python phraseExtraction.py final/postag/all/sourceAlignment.txt final/postag/all/targetAlignment.txt
# python findTranslationProbability.py phrases.txt
# mv translationProbabilitySourceGivenTarget.txt final/postag/all/translationProbabilitySourceGivenTarget.txt
# mv translationProbabilityTargetGivenSource.txt final/postag/all/translationProbabilityTargetGivenSource.txt
# python languageModelInput.py final/postag/all/trainid.txt final/postag/all/trainS.txt
# python languageModelInput.py final/postag/all/trainkr.txt final/postag/all/trainT.txt
# python languageModelInput.py final/postag/all/testid.txt final/postag/all/testS.txt
# python languageModelInput.py final/postag/all/testkr.txt final/postag/all/testT.txt
# tar -czvf final/postag/all/trainS.gz final/postag/all/trainS.txt
# tar -czvf final/postag/all/trainT.gz final/postag/all/trainT.txt
# ./../boost_1_55_0/mosesdecoder/irstlm-5.80.08/trunk/src/ngt -i="gunzip -c final/postag/all/trainS.gz" -n=3 -o=final/postag/all/train.www -b=yes
# ./../boost_1_55_0/mosesdecoder/irstlm-5.80.08/trunk/src/tlm -tr=final/postag/all/train.www -n=3 -lm=wb -o=final/postag/all/trainS.lm
# ./../boost_1_55_0/mosesdecoder/irstlm-5.80.08/trunk/src/ngt -i="gunzip -c final/postag/all/trainT.gz" -n=3 -o=final/postag/all/train.www -b=yes
# ./../boost_1_55_0/mosesdecoder/irstlm-5.80.08/trunk/src/tlm -tr=final/postag/all/train.www -n=3 -lm=wb -o=final/postag/all/trainT.lm
# python finalScore.py final/postag/all/translationProbabilityTargetGivenSource.txt final/postag/all/trainS.lm final/postag/all/finalTranslationProbabilityTargetGivenSource.txt
# python finalScore.py final/postag/all/translationProbabilitySourceGivenTarget.txt final/postag/all/trainT.lm final/postag/all/finalTranslationProbabilitySourceGivenTarget.txt
# python stackDecoder.py final/postag/all/finalTranslationProbabilityTargetGivenSource.txt final/postag/bukuTtxt.txt
# mv translation.txt final/postag/all/bukuKoreaTranslation.txt
# python stackDecoder.py final/postag/all/finalTranslationProbabilitySourceGivenTarget.txt final/postag/bukuStxt.txt
# mv translation.txt final/postag/all/bukuIndonesiaTranslation.txt

# python stackDecoder.py final/postag/all/finalTranslationProbabilityTargetGivenSource.txt final/postag/subtitleTtxt.txt
# mv translation.txt final/postag/all/subtitleKoreaTranslation.txt
# python stackDecoder.py final/postag/all/finalTranslationProbabilitySourceGivenTarget.txt final/postag/subtitleStxt.txt
# mv translation.txt final/postag/all/subtitleIndonesiaTranslation.txt

# python stackDecoder.py final/postag/all/finalTranslationProbabilityTargetGivenSource.txt final/postag/bukusubtitleTtxt.txt
# mv translation.txt final/postag/all/bsKoreaTranslation.txt
# python stackDecoder.py final/postag/all/finalTranslationProbabilitySourceGivenTarget.txt final/postag/bukusubtitleStxt.txt
# mv translation.txt final/postag/all/bsIndonesiaTranslation.txt

# print "ID - KR"
# countBLEUfromFile("final/postag/bukuT.txt","final/combine_all/particle_only/temp/verb/bukuIndonesiaTranslation.txt")
print "KR - ID"
countBLEUfromFile("final/postag/bukuS.txt","final/combine_all/particle_only/temp/verb/bukuKoreaTranslation.txt")

# print "ID - KR"
# countBLEUfromFile("final/postag/subtitleT.txt","final/combine_all/particle_only/temp/verb/subtitleIndonesiaTranslation.txt")
print "KR - ID"
countBLEUfromFile("final/postag/subtitleS.txt","final/combine_all/particle_only/temp/verb/subtitleKoreaTranslation.txt")

# print "ID - KR"
# countBLEUfromFile("final/postag/bukusubtitleT.txt","final/combine_all/particle_only/temp/verb/bsIndonesiaTranslation.txt")
print "KR - ID"
countBLEUfromFile("final/postag/bukusubtitleS.txt","final/combine_all/particle_only/temp/verb/bsKoreaTranslation.txt")
