import os, sys, logging, requests, json
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'flaskstuff'))
from flask import Flask, request, jsonify
from models.device import Device
from gcm import GCM
from gcm.gcm import GCMNotRegisteredException, GCMUnavailableException, GCMInvalidRegistrationException
from auth_data import app_keys

app = Flask(__name__) 

@app.route("/register", methods = ['POST'])
def register():
    device = Device(key=Device.generate_key(request.json['id']))
    device.id_gcm = request.json['id_gcm']
    device.os = request.json['os']
    device.language = request.json['language']
    device.put()
    return jsonify( { 'status' : 'success' } ) , 200

@app.route("/check_new_issue", methods = ['GET'])
def check_new_issue():
    req = requests.get(url='http://www.themagpi.com/mps_api/mps-api-v1.php?mode=list_issues')
    json_issues = json.loads(req.text)
    last_issue = json_issues['data'][0]
    devices = Device.query().fetch()
    gcm = GCM(app_keys['gcm'])
    data = {}
    data['id'] = '19'
    data['editorial'] = last_issue['editorial'].encode('utf8')
    data['title'] = last_issue['title']
    data['link'] = last_issue['pdf']
    data['image'] = last_issue['cover']
    data['date'] = last_issue['date']
    for device in devices:
        retry = True
        while retry:
            try:
                gcm.plaintext_request(registration_id=device.id_gcm, data=data)
                retry = False
            except GCMNotRegisteredException:
                retry = False
            except GCMInvalidRegistrationException:
                retry = False
            except GCMUnavailableException:
                retry = True
    return jsonify( { 'status' : 'success' } ) , 200
if __name__ == "__main__":
    app.run()