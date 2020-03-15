from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting

import KeywordExtract.ExtractKeyword
import EmojiText.EmojiVec
import json

import urllib
import requests

AGENT = "/agent?sentence="
PREFIX = "/agent?sentence="
RETURN_LIMIT = 5

count = 0
emoji2Vec = EmojiText.EmojiVec.EmojiVec()

# Create your views here.
def index(request):
    global count
    return render(request, "index.html")
    # return HttpResponse('Hello from Python!')

def takeScore(x):
    return x[1]

def f(request):
    '''global emoji2Vec
    print("Testing:" + str(count))
    print("XXXX: accepted:" + request.get_full_path())
    sentence = getSentence(request.get_full_path())
    print("Received sentence:" + sentence)

    ans = []
    for word in KeywordExtract.ExtractKeyword.extractKeyword(sentence):
        print("extractKeyword:" + word)
        link, score = emoji2Vec.getEmoji(word)
        print("emoji:" + link)
        ans.append((link, score))
    if len(ans) > RETURN_LIMIT:
        ans.sort(reverse=True, key=takeScore)
        ans = ans[:RETURN_LIMIT]
    x = json.dumps({"emojis":ans})

    print("sending response...")

    res = HttpResponse(x, content_type="application/json")
    res['Access-Control-Allow-Origin'] = '*'
    '''
    url = "http://localhost:7777/agent"
    data = urllib.parse.urlencode({"sentence":getSentence(request.get_full_path())})
    r = requests.get(url, data)
    res = HttpResponse(r.text, content_type="application/json")
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
