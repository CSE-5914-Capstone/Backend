import csv
import os
import json

def csvtojson(inputfile, outputfile):
    data = []
    with open(inputfile, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        data = [row for row in csvreader]

    with open(outputfile, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)


if __name__ == "__main__":
    inputcsv = 'tracks_features.csv'
    outputjson = 'example.json'

    csvtojson(inputcsv, outputjson)