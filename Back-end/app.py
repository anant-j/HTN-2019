from flask import Flask, request, jsonify
from flask_restful import Api
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_cors import CORS 
from ingest import TDApi
import json
from flask import Blueprint
from flask import jsonify
import random

app = Flask(__name__)
api = Api(app)

tdapi = TDApi()

uid = None
budget = 0.0
alerts = {

}

default_page = Blueprint('default_page', __name__)

@default_page.route('/')
def index():
    return jsonify({'Status':'This site is working'})


class UserData(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help='invalid id')
        parser.add_argument('budget', required=True, help='invalid id')
        data = parser.parse_args()
        global uid
        global budget
        uid = data.user_id
        budget = float(data.budget)
        type(uid)
        alerts['Info'] = tdapi.get_info(uid)
        alerts['Info']['budget'] = budget
        update()
        print("yes")
        return {
            'user_id' : data.user_id
        }


class AlertSystem(Resource):
    def get(self):
        update()
        return json.dumps(alerts)


def update():
    # start this by calling it once we get the UID
    transactions = tdapi.split_monthly(tdapi.get_past_transactions(uid))
    current_spent = tdapi.total_monthly_spending(transactions['9'])
    predicted_spent = tdapi.predicted_monthly_spending(transactions['9'])
    if current_spent > budget:
        alerts['OverBudget'] = {'Amount': current_spent - budget}

    elif predicted_spent > budget:
        alerts['PredictedOverBudget'] = {'Amount': predicted_spent - budget}

    fraud, not_fraud = tdapi.get_outliers(transactions['9'])
    if len(fraud) > 0:
        alerts['PotentialFraud'] = {'Amount': fraud[0]}
    
    if len(not_fraud) > 0:
        alerts['Overspending'] = {'Amount': not_fraud[0]}


CORS(app)

#API HOME PAGE

app.register_blueprint(default_page)

#User resources
api.add_resource(UserData, '/users')
api.add_resource(AlertSystem, '/alerts')

if __name__ == '__main__':
    app.run(debug=True)
