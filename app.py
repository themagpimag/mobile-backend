import os, sys, logging
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'flaskstuff'))
from flask import Flask, request, jsonify
from models.device import Device

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
    pass

if __name__ == "__main__":
    app.run()