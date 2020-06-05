from sklearn.neighbors import NearestNeighbors
import spacy
import numpy
import pickle
import google.cloud.firestore
import random
import sys
import json
import os

SPACE_PATH = "EmojiText/emojispace"
NAME2LINK_PATH = "EmojiText/emojilib"

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
        temp = json.load(f)
        temp['private_key'] = os.environ['FIRECLOUD_KEY']
        print(temp)
        f.close()
        f = open('EmojiText/auth.json', 'w')
        json.dump(temp, f)
        f.close()
        print(json.load(open("EmojiText/auth.json")))
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
        for word in listOfWords:
            listOfSanitizedWordsRef.append(self.db.collection("vectors").document(word))
        allEmbeds = list(self.db.get_all(listOfSanitizedWordsRef))
        nonempty = []
        for embed in allEmbeds:
            embed = embed.to_dict()
            if not embed == None:
                nonempty.append(embed["0"])
        return self.getEmojiForListOfWordEmbeddings(numpy.array(nonempty))
