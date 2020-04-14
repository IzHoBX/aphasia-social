from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting

import KeywordExtract.ExtractKeyword
import EmojiText.EmojiVec
import json

AGENT = "/agent?sentence="
PREFIX = "/agent?sentence="
OTHER_PREFIX = "/other"
RETURN_LIMIT = 5

ABSTRACT_LIST = ["high", "my", "a", "Nobita", "feel", "Doraemon", "go", "all", "the"]

# Create your views here.
def index(request):
    return render(request, "index.html")
    # return HttpResponse('Hello from Python!')

def takeScore(x):
    return x[1]

def f(request):
    if request.get_full_path().index(OTHER_PREFIX) == 0:
        x = json.dumps({"res":"awesome"})
        res = HttpResponse(x, content_type="application/json")
        res['Access-Control-Allow-Origin'] = '*'
        return res
    emoji2Vec = EmojiText.EmojiVec.EmojiVec()
    print("XXXX: accepted:" + request.get_full_path())
    sentence = getSentence(request.get_full_path())
    print("Received sentence:" + sentence)

    ans = {}
    # assumes punctuation sanitization is done here
    listOfKeywords = KeywordExtract.ExtractKeyword.extractKeyword(sentence)
    for i in range(0, len(listOfKeywords)):
        if listOfKeywords[i] in ABSTRACT_LIST:
            listOfKeywords = listOfKeywords[:i] + listOfKeywords[i+1:]
            continue
        if (not listOfKeywords[i].find("-") == -1) and (not listOfKeywords[i].find("-") == 0) and (not listOfKeywords[i].find("-") == len(listOfKeywords[i])-1):
            temp = listOfKeywords[i].split("-")
            listOfKeywords = listOfKeywords[:i] + listOfKeywords[i+1:]
            listOfKeywords += temp
    listOfKeywords = list(set(listOfKeywords))
    for word in ABSTRACT_LIST:
        if word in listOfKeywords:
            listOfKeywords.remove(word)
    ans = {}
    for (link, score) in emoji2Vec.getEmojiForListOfWords(listOfKeywords):
        if (not link in ans) or ans[link] > score:
            ans[link] = score
    anslist = []
    for link, score in ans.items():
        anslist.append((link, score))
    if len(anslist) > RETURN_LIMIT:
        anslist.sort(key=takeScore)
        anslist = anslist[:RETURN_LIMIT]
    x = json.dumps({"emojis":anslist})

    print("sending response...")

    res = HttpResponse(x, content_type="application/json")
    res['Access-Control-Allow-Origin'] = '*'

    return res


def getSentence(inx):
    inx = inx[len(PREFIX):]
    for i in range(0, len(inx)):
        if inx[i] == "+":
            inx = inx[:i]+ " "+inx[i+1:]
    return inx


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
