from functools import wraps
from flask import g, request, redirect, url_for, session
import requests
import urllib.parse


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(anime):

    url = f"https://api.jikan.moe/v3/search/anime?q={anime}&page=1"
    response = requests.get(url)
    
    quote = response.json()
    
    return {
        "name": response.json()['results'][0]['title'],
        "sypnosis":  response.json()['results'][0]['synopsis'],
        "image": response.json()['results'][0]['image_url']
        }
        