from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting

import KeywordExtract.ExtractKeyword
import EmojiText.EmojiVec
import json

AGENT = "/agent?sentence="
PREFIX = "/agent?sentence="
RETURN_LIMIT = 5

# Create your views here.
def index(request):
    return render(request, "index.html")
    # return HttpResponse('Hello from Python!')

def takeScore(x):
    return x[1]

def f(request):
    emoji2Vec = EmojiText.EmojiVec.EmojiVec()
    print("XXXX: accepted:" + request.get_full_path())
    sentence = getSentence(request.get_full_path())
    print("Received sentence:" + sentence)

    ans = {}
    listOfKeywords = KeywordExtract.ExtractKeyword.extractKeyword(sentence)
    for i in range(0, len(listOfKeywords)):
        if (not listOfKeywords[i].find("-") == -1) and (not listOfKeywords[i].find("-") == 0) and (not listOfKeywords[i].find("-") == len(listOfKeywords[i])-1):
            temp = listOfKeywords[i].split("-")
            for t in temp:
                listOfKeywords.append(t)
            listOfKeywords = listOfKeywords[:i] + listOfKeywords[i+1:]
    listOfKeywords = list(set(listOfKeywords))
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
