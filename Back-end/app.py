from flask import Flask, request, jsonify
from flask_restful import Api
from flask import jsonify
from views import views
from resources import resources 
from flask_cors import CORS 
from views import views
import threading
from ingest import TDApi

app = Flask(__name__)
api = Api(app)

tdapi = TDApi()

uid = None
budget = 0.0
alerts = []

def update():
    # start this by calling it once we get the UID
    threading.Timer(15, update).start()
    transactions = tdapi.split_monthy(tdapi.get_past_transactions(uid))
    current_spent = tdapi.total_monthly_spending(transactions['09'])
    predicted_spent = tdapi.predicted_monthly_spending(transactions['09'])
    if current_spent > budget:
        alerts.append({'OverBudget': {'Amount': current_spent - budget}})
    elif predicted_spent > budget:
        alerts.append({'PredictedOverBudget': {'Amount': predicted_spent - budget}})

    


CORS(app)

#API HOME PAGE

app.register_blueprint(views.default_page)

#User resources
api.add_resource(resources.UserData, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
