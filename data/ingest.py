import requests
import json
import time
import datetime
import numpy as np
from operator import itemgetter

base_url = 'https://api.td-davinci.com/api/'
key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMWI5ZjZhZmEtMWQwOS0zMjE2LTllNjAtNzVjYWIxMDY3OTdiIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiJlNDJlMTUwNy04MWQwLTRhYjgtODQ4NC1lZGU0ZTA3ZmM5MTYifQ.h2o4wV95JYMfEiNQDj8EKOxN_l463_64gHC6P8JOPiQ'

def get_past_transactions(user_id):
    url = base_url + 'customers/{}/transactions'.format(user_id) 
    headers = {'Authorization': key}
    response = requests.get(url, headers=headers)
    response_dict = response.json()
    if response_dict['statusCode'] != 200:
        raise ValueError('Response status is {}, not 200'.format(response_dict['statusCode']))

    # prune future
    """all_transaction_list = response_dict['result']
    current_time = datetime.datetime.now()
    past_transaction_list = []
    for transaction in all_transaction_list:
        date_string
        transaction_time = datetime.datetime.strptime(transaction['originationDateTime'].split('.')[0], '%Y-%m-%dT%H:%M:%SZ')
        if transaction_time < current_time:
            past_transaction_list.append(transaction)
    """
    return response_dict['result']

def split_monthy(transactions):
    months = {}
    for transaction in transactions:
        month = str(datetime.datetime.strptime(transaction['originationDateTime'].split('T')[0], '%Y-%m-%d').month)
        if month not in months:
            months[month] = []

        months[month].append(transaction)

    return months

def get_high_transactions_count(monthly_transaction_list):
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

def predicted_monthly_spending(monthly_transaction_list):
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
    return (m * 1 + b)

