from steam import Steam
from decouple import config
import json
import os
import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from requests_aws4auth import AWS4Auth
from credentials import *

# https://pypi.org/project/python-steam-api/ API document reference
# STEAM_API_KEY is my Steam domain API Key
S_Key = config("STEAM_API_KEY")
steam = Steam(S_Key)

# enter in your steam account ID below
steam_account_ID = "000000000000"
user = steam.users.get_user_recently_played_games(steam_account_ID)

#get user owned games
games_response = steam.users.get_owned_games(steam_account_ID)

for game in games_response:
    games = game[id]

def get_games(movie_title, game_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + genius_token}
    search_url = base_url + '/search'
    data = {'name': song_name + ' ' + movie_title}
    response = requests.get(search_url, data=data, headers=headers)

    game_info = None
    for game in response.json()['apps']['name']:
        if game_name.lower() in game['data']['short_description'].lower():
            game_info = hit
            break
    
    if game_info:
        game_url = game_info['data']['website']
        page = requests.get(game_url)
        html = BeautifulSoup(page.text, 'html.parser')
        return html.find('div', class_='game').get_text()

    return None


