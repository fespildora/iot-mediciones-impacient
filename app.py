from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
import string
import wiotp.sdk.application
import base64 

app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/api/mediciones', methods=['GET'])
def put_mediciones():
    import random 
    myConfig = wiotp.sdk.application.parseConfigFile("application.yaml")
    client = wiotp.sdk.application.ApplicationClient(config=myConfig, logHandlers=None)

    eventId = "Temperatura"
    # Get the last events using a python dictionary to define the device
    device = {"typeId": "Temperatura", "deviceId": "Temperatura_1"}
    lastEvents = client.lec.get(device,eventId)
    Temperatura = (base64.b64decode(lastEvents.payload).decode('utf-8'))

    eventId = "Oxigeno_Sangre"
    # Get the last events using a python dictionary to define the device
    device = {"typeId": "Oximetro", "deviceId": "Oximetro_1"}
    lastEvents = client.lec.get(device,eventId)
    Oxigeno_Sangre = (base64.b64decode(lastEvents.payload).decode('utf-8'))

    eventId = "Pulsaciones"
    # Get the last events using a python dictionary to define the device
    device = {"typeId": "Oximetro", "deviceId": "Oximetro_1"}
    lastEvents = client.lec.get(device,eventId)
    Pulsaciones = (base64.b64decode(lastEvents.payload).decode('utf-8'))

    eventId = "Presion_TAD"
    # Get the last events using a python dictionary to define the device
    device = {"typeId": "Presion_Arterial", "deviceId": "Presion_Arterial_1"}
    lastEvents = client.lec.get(device,eventId)
    TAD = (base64.b64decode(lastEvents.payload).decode('utf-8'))

    eventId = "Presion_TAS"
    # Get the last events using a python dictionary to define the device
    device = {"typeId": "Presion_Arterial", "deviceId": "Presion_Arterial_1"}
    lastEvents = client.lec.get(device,eventId)
    TAS = (base64.b64decode(lastEvents.payload).decode('utf-8'))

    eventId = "FrecRespiratoria"
    # Get the last events using a python dictionary to define the device
    device = {"typeId": "Frecuencia_Respiratoria", "deviceId": "Frecuencia_Respiratoria_1"}
    lastEvents = client.lec.get(device,eventId)
    FrecRespiratoria = (base64.b64decode(lastEvents.payload).decode('utf-8'))
    # Generate a random string 
    # with 32 characters. 
    random = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) 
    data = {'ID': random,
            'Frecuenta Respiratoria': json.loads(FrecRespiratoria)["Frecuencia Respiratoria"],
            'Temperatura':json.loads(Temperatura)["Temperatura"],
            'Presion TAD':json.loads(TAD)["TAD"],
            'Presion TAS':json.loads(TAS)["TAS"],
            'Pulsaciones':json.loads(Pulsaciones)["Pulsaciones"],
            'Oxigeno en Sangre':json.loads(Oxigeno_Sangre)["Oxigeno en Sangre"],
        }
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)


@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
