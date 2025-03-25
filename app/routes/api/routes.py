from flask import Flask, Blueprint, render_template, request, jsonify
import random

api = Blueprint('api', __name__, template_folder='templates', )

charades = [
    {'id':1, 'charade':'', 'responses':[
        {'response':'', 'correct':'true'},
        {'response':'', 'correct':'false'},
        {'response':'', 'correct':'false'},
        {'response':'', 'correct':'false'},
        {'response':'', 'correct':'false'}]},
    {'id':2, 'charade':'', 'responses':[
        {'response':'', 'correct':'true'},
        {'response':'', 'correct':'false'},
        {'response':'', 'correct':'false'},
        {'response':'', 'correct':'false'},
        {'response':'', 'correct':'false'}]}
]

@api.route('/status', methods=['GET'])
def status():
    return 'The API is currently online.', 200

@api.route('/api/charades', methods=['GET'])
def random_charade():
    return jsonify(random.choice(charades))

@api.route('/api/charades/<int:id>', methods=['GET'])
def charade(id):
    if request.method == 'GET':
            
        for charade in charades:
            if charade['id'] == id:
                return jsonify(charade)
