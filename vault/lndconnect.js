const fs = require('fs');

const PATH = './lndconnect.json';

function get() {
  let uri 
  
  try {
    if (fs.existsSync(PATH)) {
      uri = JSON.parse(fs.readFileSync(PATH)).lndconnectUri
      return uri;
    }
  } catch(e) {
    console.log('Bad encoding')
  }
  return undefined;
}

function put(lndconnectUri) {
  fs.writeFileSync(PATH, JSON.stringify({lndconnectUri}));
}

module.exports = {
  get,
  put
}