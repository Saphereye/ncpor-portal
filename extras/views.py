from django.shortcuts import render, redirect
import requests
import json


def credits(request):
    quote = json.loads(requests.get("https://api.quotable.io/random").text)
    quote = [(i.capitalize(), j) for (i, j) in quote.items() if i in ["content", "author"]]
    print(quote)
    return render(
        request=request,
        template_name="credits.html",
        context={"quote": quote},
    )

def home(request):
    return redirect("/proposals/home")