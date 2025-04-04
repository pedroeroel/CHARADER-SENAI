from flask import Flask, Blueprint, render_template, request, jsonify, redirect
import firebase_admin
from firebase_admin import credentials, firestore
import os
import random
from flask_cors import CORS
import json

api = Blueprint('api', __name__, template_folder='templates', )

serviceAccountKeyContent = os.environ.get('serviceAccountKey')
serviceAccountKeyPath = 'app/routes/api/key/serviceAccountKey.json'

if serviceAccountKeyContent:
    cred = credentials.Certificate(json.loads(serviceAccountKeyContent))
elif serviceAccountKeyPath:
    cred = credentials.Certificate(serviceAccountKeyPath)
else:
    print('Error: serviceAccountKey not found.')

    cred = None


if cred:
    firebase_admin.initialize_app(cred)

else:
    print("Firebase Admin SDK couldn't initialized.")

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
        return render_template('charade-manipulation.html')
    elif request.method == 'POST':
        userCharade = request.form.get('userCharade')
        userAnswer = request.form.get('userAnswer')

        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        charades.sort(key=lambda charade: int(charade['id']))

        newID = 1

        for charade in charades:
            if int(charade['id']) == newID:
                newID += 1
            elif int(charade['id']) > newID:
                break

        try:
            register = db.collection("charades").document(f"{newID}")
            register.set({'answer': userAnswer, 'id': str(newID), 'charade': userCharade})
            e = None
        except Exception as e:
            print(f'Back-End Error: {e}')
        finally:
            if not e:
                return render_template('charade-manipulation.html', msg=f'Charade registered at ID {newID}!')
            else:
                return render_template('charade-manipulation.html', msg=f'ERROR: Something went wrong.')
            
@api.route('/api/delete-charade/<int:id>', methods=['GET',])
def delete_charade(id):

    try:
        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())
        
        charades.sort(key=lambda charade: int(charade['id']))

        for charade in charadeList:
            if charades[id-1]['id'] == id:
                charade=True
                break
            else:
                charade=False

        db.collection('charades').document(f'{id}').delete()
        

    except Exception as e:
        print(f'Error at deletion: {e}')

    if charade == True:
        
        return render_template('charade-manipulation.html', msg='Charade deleted!')

    else:
        return render_template('charade-manipulation.html', msg='Error at deletion.')

@api.route('/api/edit-charade/<int:id>')
def edit_charade(id):
    if request.method == 'GET':

        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        for charade in charades:
            if charade['id'] == id:
                charade = charade
                break
        
        return render_template('charade-manipulation.html', charade_id=id, charade=charade['charade'], answer=charade['answer'])

    elif request.method == 'POST':

        userCharade = request.form.get('userCharade')
        userAnswer = request.form.get('userAnswer')

        try:
            document = db.collection('charades').document(id)
            
            new_data = {'answer': userAnswer, 'charade': userCharade}
            document.update(new_data)
        
            e = None

        except Exception as e:
            print(f'Back-End Error: {e}')

        finally:
 
            if not e:
                return render_template('charade-manipulation.html', msg=f'Charade edited at ID {id}!')
            
            else:
                return render_template('charade-manipulation.html', msg=f'ERROR: Something went wrong.')