import pickle

f = open("table.csv")

nameToLink = {}

for line in f:
    data = line.split(",")
    nameToLink[data[0]] = data[1] + "," + data[2]

pickle.dump(nameToLink, open("emojilib", "wb"))
f.close()
