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
                   'http://127.0.0.1:5000',
                   'null']

CORS(api, resources={r"/*": {'origins': allowed_origins}})

@api.route('/api', methods=['GET'])
def status():
    return 'The API is currently online.', 200

@api.route('/api/charades', methods=['GET', 'POST'])
def charade():

    if request.method == 'GET':
        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        if charades:
            return jsonify(random.choice(charades)), 200
        
        else:
            return jsonify('ERROR! Charade not found.'), 404
        
    elif request.method == 'POST':
        if not db:
            return jsonify({'message': 'ERROR! Database not connected.'}), 500

        data = request.get_json()
        userCharade = data.get('charade')
        userAnswer = data.get('answer')

        if not userCharade or not userAnswer:
            return jsonify({'message': 'ERROR! Both charade and answer are required.'}), 400

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
            return jsonify({'message': 'Charade created successfully!'}), 201
        except Exception as e:
            return jsonify({'message': f'ERROR! Could not save charade: {str(e)}'}), 500

        except Exception as e:
            print(f'Back-End Error: {e}')
        finally:
            if not e:
                return jsonify('message': f'Charade registered at ID {newID}!')
            else:
                return jsonify('message': 'ERROR! Something went wrong.')

@api.route('/api/charades/<int:id>', methods=['GET'])
def charadeByID(id):
    if request.method == 'GET':

        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        for charade in charades:
            if charade['id'] == id:
                return jsonify(charade), 200
            
        return jsonify({'error': f'Charade with ID {id} not found.'}), 404

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
            
@api.route('/api/delete-charade/<int:id>', methods=['GET'])
def delete_charade(id):
    try:
        charade_ref = db.collection('charades').document(str(id))
        charade_doc = charade_ref.get()

        if charade_doc.exists:
            charade_ref.delete()
            return render_template('charade-manipulation.html', msg=f'Charade with ID {id} deleted!')
        else:
            return render_template('charade-manipulation.html', msg=f'Error: Charade with ID {id} not found.')

    except Exception as e:
        print(f'Error at deletion: {e}')
        return render_template('charade-manipulation.html', msg='Error during deletion.')

@api.route('/api/edit-charade/<int:id>', methods=['POST', 'GET'])
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

        charades = []
        charadeList = db.collection('charades').stream()

        for charade in charadeList:
            charades.append(charade.to_dict())

        for charade in charades:
            if charade['id'] == id:
                charade = charade
                break

        try:
            document = db.collection('charades').document(f'{id}')
            
            new_data = {'answer': userAnswer, 'charade': userCharade}
            document.update(new_data)
        
            e = False

        except Exception as e:
            print(f'Back-End Error: {e}')
            return render_template('charade-manipulation.html', msg=f'ERROR: Something went wrong.')

        finally:
            return render_template('charade-manipulation.html', msg=f'Charade edited at ID {id}!', charade_id=id, charade=charade['charade'], answer=charade['answer'])
        
@api.route('/api/charades/list', methods=['GET'])
def list_charades():
    charades = []
    charadeList = db.collection('charades').stream()

    for charade in charadeList:
        charades.append(charade.to_dict())

    if charades:
        return jsonify(charades), 200
    else:
        return jsonify('ERROR! No charades found.'), 404