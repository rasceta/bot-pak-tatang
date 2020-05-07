import json

def open_json(filename):
    with open(filename, 'r') as f:
        servers = json.load(f)
    return servers

def write_json(filename, var_json):
    with open(filename, 'w') as f:
        json.dump(var_json, f, indent=4)