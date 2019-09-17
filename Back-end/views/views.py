from flask import Blueprint
from flask import jsonify

default_page = Blueprint('default_page', __name__)

@default_page.route('/')
def index():
    return jsonify({'Status':'This site is working'})

