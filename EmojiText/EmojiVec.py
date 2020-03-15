import emoji
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import spacy
import numpy
import pickle

NAME2LINK_PATH = "EmojiText/emojilib"

class EmojiVec:
    nameToLink = {}
    nlp = ""
    nrbs = ""
    indexToName = []

    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.nameToLink = pickle.load(open(NAME2LINK_PATH, "rb"))
        allVectors = []
        for name, link in self.nameToLink.items():
            token = self.nlp(name)
            if token.vector_norm == 0:
                print(name)
            else:
                allVectors.append(token.vector/token.vector_norm)
            self.indexToName.append(name)
        allVectors = numpy.array(allVectors)
        self.nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(allVectors)

    def getEmoji(self, word):
        token = self.nlp(word)
        wordEmbed = (token.vector/token.vector_norm).reshape(1, 300)
        distance, index = self.nbrs.kneighbors(wordEmbed)
        print(self.indexToName[index[0][0]])
        return self.nameToLink[self.indexToName[index[0][0]]], distance[0][0]
