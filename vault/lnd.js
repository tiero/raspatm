'use strict';

const LndGrpc = require('lnd-grpc');


class LND {
  constructor({ lndconnectUri }) {
    //let's create new instance of LND client 
    this.grpc = new LndGrpc({
      lndconnectUri
    });
  }

  async getInfo() {

    //Let's connect to LND Node
    await this.grpc.connect();
  
    const info = await this.grpc.services.Lightning
      .getInfo({})
      .catch(e => { throw e });
    //Let's disconnect
    await this.grpc.disconnect();
  
    return info;
  }

  async payInvoice({paymentRequest}) {
    await this.grpc.connect();
  
    const payment = await this.grpc.services.Lightning
      .payInvoice({paymentRequest})
      .catch(e => { throw e });
    //Let's disconnect
    await this.grpc.disconnect();
  
    return payment;
  } 
}


module.exports = LND;
