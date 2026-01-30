import json

def get_Target(category):
    with open('Data//gold_Target.json', 'r') as file:
        data = json.loads(file.read())
        return data[category]

