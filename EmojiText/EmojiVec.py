from sklearn.neighbors import NearestNeighbors
import spacy
import numpy
import pickle
import google.cloud.firestore
import random
import sys

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
        self.db = google.cloud.firestore.Client.from_service_account_json('EmojiText/auth.json')
        print("Emoji2Vec instantiated")

    def getEmoji(self, embed):
        embed = numpy.array(embed["0"]).reshape(1, 300)
        distance, index = self.nrbs.kneighbors(embed)
        print(self.indexToName[index[0][0]])
        return self.nameToLink[self.indexToName[index[0][0]]], distance[0][0]

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
            word = self.preprocessWord(word)
            if len(word) > 0:
                listOfSanitizedWordsRef.append(self.db.collection("vectors").document(word))
        allEmbeds = list(self.db.get_all(listOfSanitizedWordsRef))
        allAns = []
        for embed in allEmbeds:
            embed = embed.to_dict()
            if not embed == None:
                allAns.append(self.getEmoji(embed))
        return allAns
