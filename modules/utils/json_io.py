import json


def read_json(json_path):
    try:
        with open(json_path, 'r', encoding = 'utf-8') as f:
            data = json.loads(f.read())
            return data
    except json.decoder.JSONDecodeError:
        return {}


def write_to_json(json_path, data):
    prev_json_data = read_json(json_path)
    
    with open(json_path, 'w', encoding = 'utf-8') as f:
        json.dump(prev_json_data | data, f, indent = 4)