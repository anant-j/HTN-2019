from flask_restful import Resource, reqparsje
import json

class UserData(Resource):
    def get(self, user_id, budget):
        global uid
        global budget
        uid = user_id
        return {
            'Status' : 'Welcome to the club'
        }


class AlertSystem(Resource):
    def get(self):
        global alerts
        return json.dumps(alerts)