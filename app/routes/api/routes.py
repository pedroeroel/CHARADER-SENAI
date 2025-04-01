from flask import Flask, Blueprint, render_template, request, jsonify, current_app
import firebase_admin
from firebase_admin import credentials, firestore
import random
from flask_cors import CORS

api = Blueprint('api', __name__, template_folder='templates', )

cred = credentials.Certificate("app/routes/api/static/key/serviceAccountKey.json")
firebase_admin.initialize_app(cred) 

db = firestore.client()

charades = []
charadeList = db.collection('charades').stream()

for charade in charadeList:
    charades.append(charade.to_dict())

allowed_origins = ['https://charader-senai.vercel.app/',
                   'http://127.0.0.1:5000']

CORS(api, resources={r"/*": {'origins': allowed_origins}})

@api.route('/api', methods=['GET'])
def status():
    return 'The API is currently online.', 200

@api.route('/api/charades', methods=['GET'])
def random_charade():

    if charades:
        return jsonify(random.choice(charades)), 200
    
    else:
        return jsonify('ERROR! Charade not found.'), 404

@api.route('/api/charades/<int:id>', methods=['GET'])
def charade(id):
    if request.method == 'GET':
            
        for charade in charades:
            if charade['id'] == id:
                return jsonify(charade)
