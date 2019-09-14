const fetch = require('node-fetch')
const key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMWI5ZjZhZmEtMWQwOS0zMjE2LTllNjAtNzVjYWIxMDY3OTdiIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiJlNDJlMTUwNy04MWQwLTRhYjgtODQ4NC1lZGU0ZTA3ZmM5MTYifQ.h2o4wV95JYMfEiNQDj8EKOxN_l463_64gHC6P8JOPiQ'
const request= require('request');

const options = {
    url: 'https://api.td-davinci.com/api/customers/4806f34e-93a6-4e2f-9e41-5ee9f0d24f14/transactions',
    method: 'GET',
    headers: {
        'Authorization': key
    }
};
console.log(options.url);
request(options, function(err, res, body) {
    let json = JSON.parse(body)
    console.log('fsdlhfdlsj');
    var transactions = json.result;
    var currentTime = new Date;
    transactions.forEach(function(transaction) {
        console.log('works');
        var time = new Date(transaction.originationDateTime);
        if (currentTime >= time) {
            //snap.ref.child('transactions').push(transaction);
        }
    })
});
