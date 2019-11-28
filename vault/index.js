'use strict';

// import libs
const bodyParser = require('body-parser');
const express = require('express');
//Import files
const lndconnect = require('./lndconnect');
const Lnd = require('./lnd');
//App Express
const app = express();
// Declare port 
const port = process.env['PORT'] || 8000;

app.use(bodyParser.json());

//Connect the App to a LND instance
app.post('/connect', (req, res) => {
  if (req.body.lndconnectUri) {
    const { lndconnectUri } = req.body;

    try {
      lndconnect.put(lndconnectUri);
    } catch(e) {
      console.log(e);
      return res.status(500).send('Error');
    }

    return res.status(200).send('Payout service started');
  } else {
    return res.status(404).send('Missing params');
  }

})
// Get LND Info useful for other peer to connect
app.get('/info', (_, res) => {

  const lndconnectUri = lndconnect.get();
  if (!lndconnectUri)
    return res.status(500).send('Vault needs LND_CONNECT_URI being set via POST /connect');

  const lnd = new Lnd({ lndconnectUri });
  lnd.getInfo()
    .then(info => res.status(200).json(info))
    .catch(e => {
      console.log(e)
      return res.status(500).send('Error')
    });

});


app.post('/payout', (req,res) => {
  if (!req.body.invoice)
    return res.status(404).send('Missing params');
  
  const { invoice } = req.body;

  const lndconnectUri = lndconnect.get();
  if (!lndconnectUri)
    return res.status(500).send('Vault needs LND_CONNECT_URI being set via POST /connect');
  
  //do payout here
  const lnd = new Lnd({ lndconnectUri });
  lnd.payInvoice({paymentRequest:invoice})
  .then(payment => res.status(200).json(payment))
  .catch(e => {
    console.log(e)
    return res.status(500).send('Error')
  });

})

app.listen(port, () => console.log(`🏦 Vault listening on port ${port}!`));


process.on('unhandledRejection', (reason, p) => {
  p.catch(err => {
    console.error('Exiting due to unhandled rejection!')
    console.error(err)
    process.exit(1)
  })
})

process.on('uncaughtException', err => {
  console.error('Exiting due to uncaught exception!')
  console.error(err.stack)
  process.exit(1)
})
