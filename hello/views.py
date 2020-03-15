from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting

AGENT = "/agent"
count = 0


# Create your views here.
def index(request):
    global count
    return render(request, "index.html")
    # return HttpResponse('Hello from Python!')

def f(request):
    print(request.path)
    x = {"a":"B"}
    x = json.dumps(x)
    return HttpResponse(x, content_type="application/json")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
