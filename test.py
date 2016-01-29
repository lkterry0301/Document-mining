#Lab1

#Another thing we forgot to add is the class labels as provided in the TOPICS and PLACES tabs of each article

import nltk
from nltk import stem
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("data/reut2-000.sgm"),"html.parser")
stemmer = stem.porter.PorterStemmer() 
Vocabulary = {}
Freq = []
#print soup.prettify()


for doc in soup.find_all("reuters"):
	id = doc.get("newid")
	#print id
	freq = {}
	if doc.find("body") is not None:
		words = nltk.word_tokenize(doc.find("body").string)
		for word in words:
			word = word.lower()
			word = stemmer.stem(word) #get words stemmed
			if word not in freq:
				if word not in Vocabulary:
					Vocabulary[word] = 1
				else:
					Vocabulary[word] += 1
				freq[word] = 1
			else:
				freq[word] += 1
	Freq.append(freq)

for key in Vocabulary.keys():
	if Vocabulary[key] == 1:
		del Vocabulary[key]
	else:
		print key

for freq in Freq:
	vector = []
	#print freq
	for key in Vocabulary:
		if key in freq:
			vector.append(freq[key])
		else:
			vector.append(0)
	#print vector


