# please run this file from EmojiText directory
import pickle
import spacy
import numpy
from sklearn.neighbors import NearestNeighbors

SPACE_PATH = "emojispace"
NAME2LINK_PATH = "emojilib"

nameToLink = pickle.load(open(NAME2LINK_PATH, "rb"))
nlp = spacy.load("en_core_web_md")
allVectors = []
indexToName = []

for name, link in nameToLink.items():
    if "flag:" in name:
        name = name[len("flag:""):]
    token = nlp(name)
    if token.vector_norm == 0:
        print(name)
    else:
        allVectors.append(token.vector)
    indexToName.append(name)
allVectors = numpy.array(allVectors)
nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(allVectors)
pickle.dump([nbrs, indexToName], open(SPACE_PATH, "wb"))
