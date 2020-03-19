from sklearn.neighbors import NearestNeighbors
import spacy
import numpy
import pickle
import google.cloud.firestore
import random
import sys
import KeywordExtract.ExtractKeyword

SPACE_PATH = "EmojiText/emojispace"
NAME2LINK_PATH = "EmojiText/emojilib"

ABSTRACT_LIST = ["high", "my", "a", "Nobita", "feel", "Doraemon", "go", "all", "the"]


class EmojiVec:
    nameToLink = {}
    nlp = ""
    nrbs = ""
    indexToName = []
    db = ""

    def __init__(self):
        print("loading model")
        model = pickle.load(open(SPACE_PATH, "rb"))
        self.indexToName = model[1]
        self.nrbs = model[0]
        self.nameToLink = pickle.load(open(NAME2LINK_PATH, "rb"))
        self.db = google.cloud.firestore.Client.from_service_account_json('EmojiText/auth.json')
        print("Emoji2Vec instantiated")

    def getEmojiForListOfWordEmbeddings(self, twoDNumpyArray):
        distance, index = self.nrbs.kneighbors(twoDNumpyArray)
        link = []
        for i in range(0, len(index)):
            name = self.indexToName[index[i][0]]
            print(name)
            link.append([self.nameToLink[name], distance[i][0]])
        return link

    def preprocessWord(self, word):
        if not word[-1].isalpha():
            word = word[:-1]
        if len(word) > 0 and not word[0].isalpha():
            word = word[1:]
        word = word.lower()
        return word

    def getEmojiForListOfWords(self, listOfWords):
        listOfSanitizedWordsRef = []
        nonempty = []
        for word in listOfWords:
            res = self.db.collection("vectors").document(word).get()
            res = res.to_dict()
            if not res == None:
                print(word)
                nonempty.append(res["0"])
        print("------")
        return self.getEmojiForListOfWordEmbeddings(numpy.array(nonempty))

emoji2Vec = EmojiVec()
listOfKeywords = KeywordExtract.ExtractKeyword.extractKeyword(input("enter sentence:"))
for i in range(0, len(listOfKeywords)):
    if (not listOfKeywords[i].find("-") == -1) and (not listOfKeywords[i].find("-") == 0) and (not listOfKeywords[i].find("-") == len(listOfKeywords[i])-1):
        temp = listOfKeywords[i].split("-")
        listOfKeywords = listOfKeywords[:i] + listOfKeywords[i+1:]
        listOfKeywords += temp
listOfKeywords = list(set(listOfKeywords))
for word in ABSTRACT_LIST:
    if word in listOfKeywords:
        listOfKeywords.remove(word)

print(emoji2Vec.getEmojiForListOfWords(listOfKeywords))
