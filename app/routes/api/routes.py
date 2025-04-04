from flask import Flask, Blueprint, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
import random
from flask_cors import CORS

api = Blueprint('api', __name__, template_folder='templates', )

serviceAccountKey = os.environ.get('serviceAccountKey', 'app/routes/api/key/serviceAccountKey.json')
cred = credentials.Certificate(serviceAccountKey)

firebase_admin.initialize_app(cred) 

db = firestore.client()

allowed_origins = ['https://charader-senai.vercel.app/',
                   'http://127.0.0.1:5000']

CORS(api, resources={r"/*": {'origins': allowed_origins}})

@api.route('/api', methods=['GET'])
def status():
    return 'The API is currently online.', 200

@api.route('/api/charades', methods=['GET'])
def random_charade():

    charades = []
    charadeList = db.collection('charades').stream()

    for charade in charadeList:
        charades.append(charade.to_dict())

    if charades:
        return jsonify(random.choice(charades)), 200
    
    else:
        return jsonify('ERROR! Charade not found.'), 404

@api.route('/api/charades/<int:id>', methods=['GET'])
def charade(id):
    if request.method == 'GET':
            
        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        for charade in charades:
            if charade['id'] == id:
                return jsonify(charade)

@api.route('/api/new-charade', methods=['GET', 'POST'])
def new_charade():
    if request.method == 'GET':

        return render_template('new-charade.html')

    elif request.method == 'POST':

        userCharade = request.form.get('userCharade')
        userAnswer = request.form.get('userAnswer')

        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        currentID = 0

        for charade in charades:
            previousID = currentID
            currentID = int(charade['id'])

            if (currentID - previousID) > 1:
                newID = previousID + 1
                break
            else:
                newID = currentID + 1

        try:
                
            register = db.collection("charades").document(f"{newID}")
            register.set({'answer': userAnswer, 'id': newID, 'charade': userCharade})
        
            e = None

        except Exception as e:
            print(f'Back-End Error: {e}')

        finally:
 
            if not e:
                return render_template('new-charade.html', msg=f'Charade registered in the ID {newID}!')
            
            else:
                return render_template('new-charade.html', msg=f'ERROR: Something went wrong.')
            