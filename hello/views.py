from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting

AGENT = "/agent?sentence="

count = 0


# Create your views here.
def index(request):
    global count
    count += 1
    print("asdvsafvasfgasd" + str(count))
    return render(request, "index.html")
    # return HttpResponse('Hello from Python!')

def f(request):
    emoji2Vec = EmojiText.EmojiVec.EmojiVec()
    sentence = getSentence(request.path)

    ans = []
    for word in KeywordExtract.ExtractKeyword.extractKeyword(sentence):
        link, score = emoji2Vec.getEmoji(word)
        ans.append((link, score))
    if len(ans) > RETURN_LIMIT:
        ans.sort(reverse=True, key=takeScore)
        ans = ans[:RETURN_LIMIT]

    x = {}
    for i in range(0, len(ans)):
        x[str(i)] = ans[i][0]
    x = json.dumps(x)

    res = HttpResponse(x, content_type="application/json")
    res['Access-Control-Allow-Origin'] = '*'

    return


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
