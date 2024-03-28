import os
import json
import time
import spotipy
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


def getAccessToken(auth):
    #clientId = '834545c65b434617a906b8ea321e7e5b'
    #clientPass = '8861fc75e1bd49c29aa035278faa6e8f'
    access = auth.get_access_token()
    return access

def getLink(song_id, accessToken):
    print('in get Link')
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    headers = {
        'Authorization': f'Bearer {accessToken}'
    }
    response = requests.get(url, headers=headers)
    print(response.content)
    if response.status_code == 200:
        track_data = response.json()
        return track_data['external_urls']['spotify']
    else:
        print("Error:", response.status_code)
        print(response.content)
        return None

def setLinks(playlist, authenticate, accessToken):
    print('In set Links')
    songList = []
    #call method to get songs
    for song in playlist['Playlist Songs with attributes']:
        print(song)
        newObj = dict()
        newObj['Song Name'] = song['track_name']
        #newObj['Artist'] = song['track_artist']
        newObj['Link'] = getLink(song['track_id'], accessToken)
        songList.append(newObj)
    print('about to return links')
    return songList
    
    
#if __name__ == '__main__':    
