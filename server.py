import os.path
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def save(id, config):
    with open(id + '.txt', 'wb') as outfile:
        outfile.write(config)
        outfile.close

def load(id):
    with open(id + '.txt') as inputfile:
        config = inputfile.read()
        inputfile.close()
        return config


@app.route('/config', methods=['GET', 'POST'])
def config():
    id = request.args.get('id')

    if request.method == 'POST':
        save(id, request.get_data())
        return "", 200
    else:
        if os.path.isfile(id + '.txt'):
            return load(id), 200
        else:
            return "", 404



def register(new_device):
    json_file = open('devices.txt')
    devices = json.load(json_file)
    json_file.close()
    new_devices = []

    already_exists = False
    for device in devices:
        if device['id'] == new_device['id']:
            new_devices.append(new_device)
            already_exists = True
        else:
            new_devices.append(device)

    if not already_exists:
        new_devices.append(new_device)
        
    with open('devices.txt', 'w') as outfile:
        json.dump(new_devices, outfile)

def un_register(id):
    json_file = open('devices.txt')
    devices = json.load(json_file)
    json_file.close()

    new_devices = []
    for device in devices:
        if device['id'] != id:
            new_devices.append(device)
    
    with open('devices.txt', 'w') as outfile:
        json.dump(new_devices, outfile)

def get_devices():
    with open('devices.txt') as inputfile:
        devices = inputfile.read()
        inputfile.close()
        return devices


@app.route('/device', methods=['GET', 'POST', 'DELETE'])
def device():
    if request.method == 'POST':
        register(request.get_json(force=True))
        return "", 200
    elif request.method == 'GET':
        return get_devices(), 200
    elif request.method == 'DELETE':
        id = int(request.args.get('id'))
        un_register(id)
        return "", 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)