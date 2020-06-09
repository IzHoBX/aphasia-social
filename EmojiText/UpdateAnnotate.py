import pickle

f = open("table.csv")

nameToLink = {}

for line in f:
    data = line.split(",")
    indexForLink = 1
    while not "data:image/png;base64" in data[indexForLink]:
        indexForLink += 1
    name = "".join(map(lambda x: x + " ", data[:indexForLink]))[:-1]
    nameToLink[name] = data[indexForLink] + "," + data[indexForLink+1]

pickle.dump(nameToLink, open("emojilib", "wb"))
f.close()
