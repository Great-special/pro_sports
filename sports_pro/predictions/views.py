from django.conf import settings
from django.shortcuts import render


import requests

# Create your views here.

def index(request):
    url = "https://livescore6.p.rapidapi.com/news/v2/list"

    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    data = response.json()
    context = {
        'categories':data['categories'],
        'topstories':data['topStories'],
        'homearticle':data['homepageArticles'],
    }
    return render(request, 'predictions.html', context)
