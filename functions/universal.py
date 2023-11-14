import json

def load_json(file_name: str) -> json:
    '''Load json data'''
    with open(file_name, encoding='utf8') as input:
        data = json.load(input)
    return data