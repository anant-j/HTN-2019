const functions = require('firebase-functions');

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
const admin = require('firebase-admin');
const request = require('request')

const key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMWI5ZjZhZmEtMWQwOS0zMjE2LTllNjAtNzVjYWIxMDY3OTdiIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiJlNDJlMTUwNy04MWQwLTRhYjgtODQ4NC1lZGU0ZTA3ZmM5MTYifQ.h2o4wV95JYMfEiNQDj8EKOxN_l463_64gHC6P8JOPiQ'

admin.initializeApp({
    credential: admin.credential.applicationDefault(),
    databaseURL: 'https://hackthenorth-2019.firebaseio.com'
});

exports.getUserData = functions.database.ref('/').onCreate(async(snap, context) => {
    if (snap.ref.parent == null) {
        snap.ref.set({
            transactions: {},
            Info: {}
        });

        const options = {
            url: 'https://api.td-davinci.com/api/customers/' + snap.val() + '/transactions',
            method: 'GET',
            headers: {
                'Authorization': key
            }
        };

        request("https://google.com", function(err, res, body) {
            console.log(">>> This works!");
        });

        console.log(">>>" + options.url);

        request(options, function(err, res, body) {
            console.log(err);
            let json = JSON.parse(body)
            console.log('fsdlhfdlsj');
            var transactions = response.json().result;
            var currentTime = new Date;
            transactions.forEach(function(transaction) {
                console.log('yeet');
                var time = new Date(transaction.originationDateTime);
                if (currentTime >= time) {
                    snap.ref.child('transactions').push(transaction);
                }
            })
        });
        console.log(">>> request queued");
    }
    return 0;
})