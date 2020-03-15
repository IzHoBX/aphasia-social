import pickle

CODE_PREFIX = "<td class=\"code\"><a href=\""
NAME_PREFIX = "<td class=\"name\">"
CLOSING_TAG = "\"></td>"
ANDR_PREFIX = "<td class=\"andr\""
SRC = "class=\"imga\" src=\""
INVALID_CHAR = "⊛ "

ANDR_LIMIT = 3

f = open("FullTable.html")

nameToLink = {}
foundCode = False
nameTemp = ""
andrCount = 0

index = 1

for line in f:
    if not foundCode and CODE_PREFIX in line:
        linkTemp = ""
        foundCode = True
        andrCount = 0
    else:
        if NAME_PREFIX in line:
            nameTemp = ""
            for i in range(line.find(NAME_PREFIX)+len(NAME_PREFIX), len(line)):
                if line[i] == '<':
                    break
                else:
                    nameTemp += line[i]
            if INVALID_CHAR in nameTemp:
                nameTemp = nameTemp[nameTemp.find(INVALID_CHAR)+len(INVALID_CHAR):]
            if linkTemp != "":
                nameToLink[nameTemp] = linkTemp
            foundCode = False
        elif ANDR_PREFIX in line:
            andrCount += 1
            if andrCount == ANDR_LIMIT:
                linkTemp = line[line.find(SRC)+len(SRC):line.find(CLOSING_TAG)]


print("Done, found: " + str(len(nameToLink)))
pickle.dump(nameToLink, open("emojilib", "wb"))
f.close()

f = open("table.csv", "w")
for name, link in nameToLink.items():
    f.write(name+","+link+"\n")
f.close()
