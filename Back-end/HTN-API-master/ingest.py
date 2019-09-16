import requests
import json
import time
import datetime
import numpy as np
from operator import itemgetter

class TDApi:

    def __init__(self):
        self.base_url = 'https://api.td-davinci.com/api/' 
        self.key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMWI5ZjZhZmEtMWQwOS0zMjE2LTllNjAtNzVjYWIxMDY3OTdiIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiJlNDJlMTUwNy04MWQwLTRhYjgtODQ4NC1lZGU0ZTA3ZmM5MTYifQ.h2o4wV95JYMfEiNQDj8EKOxN_l463_64gHC6P8JOPiQ'
        self.headers = {'Authorization': self.key}
    
    def get_past_transactions(self, user_id):
        url = self.base_url + 'customers/{}/transactions'.format(user_id) 
        response = requests.get(url, headers=self.headers)
        response_dict = response.json()
        if response_dict['statusCode'] != 200:
            raise ValueError('Response status is {}, not 200'.format(response_dict['statusCode']))

        # prune future
        all_transaction_list = response_dict['result']
        current_time = datetime.datetime.now()
        past_transaction_list = []
        for transaction in all_transaction_list:
            transaction_time = datetime.datetime.strptime(transaction['originationDateTime'][:19], '%Y-%m-%dT%H:%M:%S')
            if transaction_time < current_time:
                past_transaction_list.append(transaction)
        
        return past_transaction_list

    def split_monthly(self, transactions):
        months = {}
        for transaction in transactions:
            month = str(datetime.datetime.strptime(transaction['originationDateTime'].split('T')[0], '%Y-%m-%d').month)
            if month not in months:
                months[month] = []

            months[month].append(transaction)

        return months

    def get_high_transactions_count(self, monthly_transaction_list):
        merchants = {}
        for transaction in monthly_transaction_list:
            if 'merchantName' in transaction:
                merchant_name = transaction['merchantName']
                if merchant_name not in merchants:
                    merchants[merchant_name] = {'totalCash': 0.0, 'transactionCount': 0}

                merchants[merchant_name]['totalCash'] += transaction['currencyAmount']
                merchants[merchant_name]['transactionCount'] += 1

        problem_merchants = {}
        for merchant in merchants:
            if merchants[merchant]['transactionCount'] >= 20:
                problem_merchants[merchant] = merchants[merchant]

        return problem_merchants

    def predicted_monthly_spending(self, monthly_transaction_list):
        transaction_pairs = []
        for transaction in monthly_transaction_list:
            date = datetime.datetime.strptime(transaction['originationDateTime'].split(':')[0], '%Y-%m-%dT%H')
            date_decimal = (date.day * 24 + date.hour) / 720 
            transaction_pairs.append((date_decimal, transaction['currencyAmount']))

        sorted_pairs = sorted(transaction_pairs, key=itemgetter(0))
        x = []
        y = []
        summed = 0
        for i in range(0, len(sorted_pairs)):
            x.append(sorted_pairs[i][0])
            summed += abs(sorted_pairs[i][1])
            y.append(summed)

        # linear regression with the lads
        x = np.array(x)
        y = np.array(y)
        A = np.vstack([x, np.ones(len(x))]).T
        m, b = np.linalg.lstsq(A, y, rcond=None)[0]
        return (m + b)

    def total_monthly_spending(self, monthly_transaction_list):
        spending = 0.0
        for transaction in monthly_transaction_list:
            spending += abs(transaction['currencyAmount'])

        return spending

    def get_outliers(self, transactions):
        x = []
        y = []
        for transaction in transactions:
            x.append(transaction['originationDateTime'])
            y.append(transaction['currencyAmount'])

        stdev = np.std(y)
        mean = np.mean(y)
        floor = mean + 1.2 * stdev
        spending_outliers = []
        for i in range(len(x)):
            if y[i] > floor:
                spending_outliers.append([x[i], y[i]])

        for outlier in spending_outliers:
            date = datetime.datetime.strptime(outlier[0].split(':')[0], '%Y-%m-%dT%H')
            date_decimal = (date.day * 24 + date.hour) / 720
            outlier[0] = date_decimal

        stdev = np.std([outlier[0] for outlier in spending_outliers])
        mean = np.mean([outlier[0] for outlier in spending_outliers])
        fraud = []
        not_fraud = []
        for outlier in spending_outliers:
            if abs(outlier[0] - mean) > stdev*2:
                fraud.append(outlier)
            else:
                not_fraud.append(outlier)

        return (fraud, not_fraud)

    def get_info(self, uid):
        response = requests.get(self.base_url + 'customers/' + uid, headers=self.headers).json()
        info = {
            'municipality': response['result']['addresses']['principalResidence']['municipality'],
            'age': response['result']['age'],
            'income': response['result']['totalIncome']
        }
        return info
