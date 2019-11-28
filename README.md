# RaspATM

## Deployment

**Mainnet**

* Run the cluster 
`$ docker-compose up -d`

* If first time create/import the wallet with a seed 
`$ docker exec -it lnd-node lncli -lnddir=/lnd/.lnd create`

* If already created, unlock if a restart
 `$ docker exec -it lnd-node lncli -lnddir=/lnd/.lnd unlock`

* Get the LNDCONNECT URI from LND node and push to the Vault service
```
$ lndconnecturi="$(docker exec lnd-node lndconnect --host=lnd  -p 10009 --url --lnddir /lnd/.lnd)"
$ curl -X POST -H 'Content-Type: application/json' -d '{"lndconnectUri":"'"${lndconnecturi}"'"}' http://raspberrypi.local:8000/connect
```

* Test info endpoint

`$ curl -X GET http://raspberrypi.local:8000/info`


