import json

f = open("PossibleWords.txt", "r")

data = f.read().split("\n")

json_object = json.dumps(data, indent=4)

with open("sample.json", "w") as outfile:
    outfile.write(json_object)