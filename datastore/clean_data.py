import json
import os

songs_30000 = json.load(open('initsongs_30000.json', encoding='utf8'))

ids = set()
newjson = []
for song in songs_30000:
    if song['track_id'] not in ids:
        ids.add(song['track_id'])
        newjson.append(song)

print(len(songs_30000))
print(len(newjson))
print(newjson[1])

with open('uniquesongs.json', 'w') as newfile:
    json.dump(newjson, newfile, indent=4)
