import json
import re
import string
import unicodedata
from datetime import datetime
import nltk
from nltk.stem import WordNetLemmatizer
from pip._vendor.pyparsing import unicode
import math
import time
import operator
# from sql_db import sql_db


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")

    return str(text)

def Normalization(doc):
    # doc = re.sub(r"(?<!\w)([A-Za-z])\.", r"\1", doc)
    doc = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", doc)
    # doc = re.sub(r"[^a-z']", " ", doc)
    # doc = (decontracted(doc))
    Regex = re.compile('[%s]' % re.escape(string.punctuation))
    doc = Regex.sub(' ', doc)
    doc = doc.replace('â€', " ")
    doc = doc.replace("â–", " ")
    doc = doc.replace('”', " ")
    doc = doc.lower()
    doc = strip_accents(doc)
    return doc


try:
	with open('../data/train.json') as f:
		data = json.load(f)
except ValueError:
	print ("error loading JSON")
BoW = []
Words = []
for i in range(0, len(data)):
    # data[i]['ingredients'] = StopWordsRemoval(data[i]['ingredients'], StopWords)
    for j in range(0, len(data[i]['ingredients'])):
        # as data is stored in the form of json object i.e. dictionary hence lemmatizing and normalizing each
        # word of ingredient in it
        data[i]['ingredients'][j] = Normalization(data[i]['ingredients'][j])
        # data[i]['ingredients'][j] = Lemmatization(data[i]['ingredients'][j])

        # if the word doesnot exist in the Bag of Words inly then is appended in the list of bag of words
        ing = (data[i]['ingredients'][j])
        Words.append(ing)
        if not (ing in BoW):
        	BoW.append(ing)

f2 = open("../data/StopWords.txt",'w')
f2.close()
f2 = open("../data/StopWords.txt",'a')
Bow_Weight = {}
for i in BoW:
	count = Words.count(i)
	if count > 1000:
		f2.write(i + "\n")
	Bow_Weight[i] = count
f2.close()
f = open("../results/Words_Weight.txt",'w')
Bow_Weight = dict(sorted(Bow_Weight.items(), key=operator.itemgetter(1), reverse=True))
f.write(str(Bow_Weight))



#                 
# f = open("../data/StopWords.txt",'r')
# data = f.read()
# data = data.split("\n")
# unique = []
# a = ''
# for i in data:
# 	if not(i in unique):
# 		unique.append(i)
# 		a =a + i + "\n"
# f = open("../data/StopWords.txt",'w')
# f.write(a)