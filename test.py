#Lab1

#Another thing we forgot to add is the class labels as provided in the TOPICS and PLACES tabs of each article

import nltk
from os import listdir
from bs4 import BeautifulSoup

stemmer = nltk.stem.porter.PorterStemmer() 
Vocabulary = {}
Freq = []
#print soup.prettify()

def get_word_frequency(soup):
    currentFreq=[]
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
    currentFreq.append(freq)
    return currentFreq
    
#ask for directory for dataset
file_path=raw_input("Please enter the directory of reuters dataset: ") 

#iterate through all files in the given directory
for file in listdir(file_path):
    soup = BeautifulSoup(open(file_path+file),"html.parser")
    Freq.append(get_word_frequency(soup))
    
for key in Vocabulary:
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


