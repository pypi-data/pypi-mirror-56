import nltk
from nltk import *
def gersyll_tocsv(path):
	from nltk.corpus import PlaintextCorpusReader
	import pandas
	from pandas import DataFrame
	corpus_root = path
	corpus = PlaintextCorpusReader(corpus_root, '.*')
	import re
	def reduce_dip(corpus_string):
		corpus_string = corpus_string.replace("Ei", "ö")
		corpus_string = corpus_string.replace("ei", "ö")
		corpus_string = corpus_string.replace("Ey", "ö")
		corpus_string = corpus_string.replace("ey", "ö")
		corpus_string = corpus_string.replace("Ay", "ö")
		corpus_string = corpus_string.replace("ay", "ö")
		corpus_string = corpus_string.replace("Ai", "ö")
		corpus_string = corpus_string.replace("ai", "ö")
		corpus_string = corpus_string.replace("Eu", "ö")
		corpus_string = corpus_string.replace("eu", "ö")
		corpus_string = corpus_string.replace("Äu", "ö")
		corpus_string = corpus_string.replace("äu", "ö")
		corpus_string = corpus_string.replace("Au", "ö")
		corpus_string = corpus_string.replace("au", "ö")
		corpus_string = corpus_string.replace("Ie", "ö")
		corpus_string = corpus_string.replace("ie", "ö")
		return corpus_string
	vowels = [' ','a','e','i','o','u','ä','ö','ü','A','E','I','O','U','Ä','Ö','Ü']
	cfd_syll = nltk.ConditionalFreqDist(
		(textname, num_syll)
		for textname in corpus.fileids()
		for num_syll in [len(w) for w in ''.join(char for char in reduce_dip(corpus.raw(fileids=textname)) if char in vowels).split()])
	syll_dataframe = DataFrame(cfd_syll)
	return syll_dataframe.to_csv(path + '\silben.csv')

def gersyll_tabulate(path):
	from nltk.corpus import PlaintextCorpusReader
	import pandas
	from pandas import DataFrame
	corpus_root = path
	corpus = PlaintextCorpusReader(corpus_root, '.*')
	import re
	def reduce_dip(corpus_string):
		corpus_string = corpus_string.replace("Ei", "ö")
		corpus_string = corpus_string.replace("ei", "ö")
		corpus_string = corpus_string.replace("Ey", "ö")
		corpus_string = corpus_string.replace("ey", "ö")
		corpus_string = corpus_string.replace("Ay", "ö")
		corpus_string = corpus_string.replace("ay", "ö")
		corpus_string = corpus_string.replace("Ai", "ö")
		corpus_string = corpus_string.replace("ai", "ö")
		corpus_string = corpus_string.replace("Eu", "ö")
		corpus_string = corpus_string.replace("eu", "ö")
		corpus_string = corpus_string.replace("Äu", "ö")
		corpus_string = corpus_string.replace("äu", "ö")
		corpus_string = corpus_string.replace("Au", "ö")
		corpus_string = corpus_string.replace("au", "ö")
		corpus_string = corpus_string.replace("Ie", "ö")
		corpus_string = corpus_string.replace("ie", "ö")
		return corpus_string
	vowels = [' ','a','e','i','o','u','ä','ö','ü','A','E','I','O','U','Ä','Ö','Ü']
	cfd_syll = nltk.ConditionalFreqDist(
		(textname, num_syll)
		for textname in corpus.fileids()
		for num_syll in [len(w) for w in ''.join(char for char in reduce_dip(corpus.raw(fileids=textname)) if char in vowels).split()])
	syll_dataframe = DataFrame(cfd_syll)
	return cfd_syll.tabulate()

print ('=========================================================')
print ('Hallo! Ich bin Gersyll, ich zahle Worte von allen Silbenmengen für alle deine Texte')
print ('Gib "gersyll_tabulate(path)" ein, um eine Tabelle zu bekommen')
print ('Gib "gersyll_tocsv(path)" ein, wenn du dein Ergebnis als csv.-Datei willst')
print ('Pfadenformat: r"DEIN\PFAD')
print ('Viel Spaß!')
