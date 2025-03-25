from flask import Flask, Blueprint, render_template, request

main = Blueprint('main', __name__, template_folder='templates', )


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')