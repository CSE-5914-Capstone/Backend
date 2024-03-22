import json
import os
import time

errorsongs = 0

def trimSong30000(fullSong):
    currsong = dict()
    currsong['track_id'] = fullSong['track_id']
    currsong['track_name'] = fullSong['track_name']
    currsong['track_album_id'] = fullSong['track_album_id']
    currsong['danceability'] = fullSong['danceability']
    currsong['energy'] = fullSong['energy']
    currsong['loudness'] = fullSong['loudness']
    currsong['liveness'] = fullSong['liveness']
    currsong['valence'] = fullSong['valence']
    currsong['tempo'] = fullSong['tempo']
    currsong['duration_ms'] = fullSong['duration_ms']
    currsong['explicit'] = True
    currsong['artists'] = [fullSong['track_artist']]

    return currsong

def trimSong1200000(fullSong):
    currsong = dict()
    currsong['track_id'] = fullSong['id']
    currsong['track_name'] = fullSong['name']
    currsong['track_album_id'] = fullSong['album_id']

    danceability = float(fullSong['danceability'])
    if danceability is None:
        return False
    else:
        currsong['danceability'] = danceability

    energy = float(fullSong['energy'])
    if danceability is None:
        return False
    else:
        currsong['energy'] = energy

    loudness = float(fullSong['loudness'])
    if loudness is None:
        return False
    else:
        currsong['loudness'] = loudness

    liveness = float(fullSong['liveness'])
    if liveness is None:
        return False
    else:
        currsong['liveness'] = liveness
    
    valence = float(fullSong['valence'])
    if valence is None:
        return False
    else:
        currsong['valence'] = valence

    tempo = float(fullSong['tempo'])
    if tempo is None:
        return False
    else:
        currsong['tempo'] = tempo
    
    duration = float(fullSong['duration_ms'])
    if duration is None:
        return False
    else:
        currsong['duration_ms'] = duration

    explicit = bool(fullSong['explicit'])
    if explicit is None:
        return False
    else:
        currsong['explicit'] = explicit

    artists = fullSong['artists']
    if artists is None:
        return False
    else:
        currsong['artists'] = artists

    return currsong

start = time.time()

songs_30000 = json.load(open(os.path.join(os.path.dirname(__file__),'initsongs_30000.json'), encoding='utf8'))

ids = set()
newjson = []
for song in songs_30000:
    currsong=dict()
    if song['track_id'] not in ids:
        ids.add(song['track_id'])
        currsong = trimSong30000(song)

        if currsong is not False:
            newjson.append(currsong)
        else:
            errorsongs += 1

middle = time.time()

print(f'30000 song dataset loaded in {middle-start} seconds ({(middle-start)/60} minutes)')

songs_1200000 = json.load(open(os.path.join(os.path.dirname(__file__),'initsongs_1200000.json'), encoding='utf8'))

for song in songs_1200000:
    currsong=dict()
    if song['id'] not in ids:
        ids.add(song['id'])
        currsong = trimSong1200000(song)

        if currsong is not False:
            newjson.append(currsong)
        else:
            errorsongs += 1

with open(os.path.join(os.path.dirname(__file__), 'uniquesongs.json'), 'w') as newfile:
    json.dump(newjson, newfile, indent=4)

end = time.time()

print(f'1200000 song dataset loaded in {end-middle} seconds ({(end-middle)/60} minutes)')

print(f'All songs loaded in {end-start} seconds ({(end-start)/60} minutes)')

print(f'Disregarded {errorsongs} bad input songs')