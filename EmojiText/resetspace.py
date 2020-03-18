# please run this file from EmojiText directory
import pickle
import spacy
import numpy
from sklearn.neighbors import NearestNeighbors

SPACE_PATH = "emojispace"
NAME2LINK_PATH = "emojilib"

nameToLink = pickle.load(open(NAME2LINK_PATH, "rb"))
nlp = spacy.load("en_core_web_lg")
allVectors = []
indexToName = []

for name, link in nameToLink.items():
    token = nlp(name)
    if token.vector_norm == 0:
        print(name)
    else:
        foundSharedVec = False
        for i in range(0, len(allVectors)):
            if numpy.array_equal(allVectors[i], token.vector):
                print(indexToName[i] + " " + name)
                foundSharedVec = True
        if not foundSharedVec:
            allVectors.append(token.vector)
            indexToName.append(name)
allVectors = numpy.array(allVectors)
nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(allVectors)
pickle.dump([nbrs, indexToName], open(SPACE_PATH, "wb"))
