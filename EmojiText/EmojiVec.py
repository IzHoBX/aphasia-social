import emoji
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

    def getEmoji(self, word):
        if not word[-1].isalpha():
            word = word[:-1]
        if len(word) > 0 and not word[0].isalpha():
            word = word[1:]
        if len(word) == 0:
            return self.nameToLink[self.indexToName[random.randrange(0, len(self.indexToName))]], sys.maxsize
        word = word.lower()
        try:
            token = self.db.collection("vectors").document(word).get().to_dict()
        except google.cloud.exceptions.NotFound:
            return self.nameToLink[self.indexToName[random.randrange(0, len(self.indexToName))]], sys.maxsize
        if token == None:# exception seems will not be raised
            return self.nameToLink[self.indexToName[random.randrange(0, len(self.indexToName))]], sys.maxsize
        token["0"] = numpy.array(token["0"])
        if not token["1"] == 0:
            wordEmbed = (token["0"]/token["1"]).reshape(1, 300)
        else:
            wordEmbed = token["0"].reshape(1, 300)
        distance, index = self.nrbs.kneighbors(wordEmbed)
        print(self.indexToName[index[0][0]])
        return self.nameToLink[self.indexToName[index[0][0]]], distance[0][0]
