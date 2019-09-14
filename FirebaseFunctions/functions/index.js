const functions = require('firebase-functions');

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
const admin = require('firebase-admin');
const fetch = require('node-fetch')

const key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMWI5ZjZhZmEtMWQwOS0zMjE2LTllNjAtNzVjYWIxMDY3OTdiIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiJlNDJlMTUwNy04MWQwLTRhYjgtODQ4NC1lZGU0ZTA3ZmM5MTYifQ.h2o4wV95JYMfEiNQDj8EKOxN_l463_64gHC6P8JOPiQ'

admin.initializeApp();

exports.getUserData = functions.database.ref().onCreate((snapshot) => {
    if (snapshot.ref.parent.key == 'Users') {
        snapshot.ref.set({
            transactions: {},
            Info: {}
        });
        var headers = {
            'Authorization': key
        }
        fetch('https://api.td-davinci.com/api/customers/' + uid + '/transactions', { method: 'GET', headers: headers})
            .then(function(response) {
                return response.json();
            })
            .then(function(responseJson) {
                var transactions = responseJson.result;
                var currentTime = new Date;
                transactions.forEach(function(transaction) {
                    var time = new Date(transaction.originationDateTime);
                    if (currentTime >= time) {
                        snapshot.ref.child('transactions').push(transaction);
                    }
                });
            });
    }
});