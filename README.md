# 4020-pub-sub-sensor

## Broker

### Setup/installing dependencies:
Assuming you have a recent(ish) python (>3.6), run the following in your terminal:
```bash
cd broker
source init_env.sh
```
This should create a virtual python environment, install the dependencies needed for this program, and install a development version of this program.

Next, if you want to run the included `update_data.py` program, you'll need to generate a keypair by doing the following (this assumes you have openssl installed):

```bash
./gen_keys.sh ex
```

To run, you can then do the following:
```bash
python -m broker.main
```

Tests can be run by navigating to `broker/tests` and running any of
the python files in there. For instance, running `update_data.py` will
simulate a sensor sending some data to the broker. And running
`client.py` will simulate some application subscribing to the broker.

### Publishing

To publish a sensor value, submit a HTTP POST request to `n4abi.com:9000/api/sensor` using a JSON Web token of the following format:

header:
```json
{"alg": "RS256", "typ": "JWT"}
```
body:
```json
{"sensortype": "type", "sensorid": "id", "value": "value"}
```
signature:
RS256 type signature. (Tyler I will help you out with this part)

### Polling

To get sensor data without subscribing, submit a HTTP GET request to `n4abi.com:9000/api/sensor`. It will return a JSON array of responses like those returned under Subscribing

### Subscribing

To subscribe to sensor values, you will need to open a websocket to `ws://n4abi.com:9000/api/subscribe`, and send a json message of the following format:

```json
{"cmd": "subscribe", "sensortype": "type", "sensorid": "id"}
```

Note that the `sensortype` and `sensorid` fields are optional. Specifying one or both fields will cause the broker to filter only requests matching those fields. 

Whenever a sensor publishes some data, you'll receive some JSON data in the following format:
```json
{"sensortype": "type", "sensorid": "id", "value": "value"}
```

### Key generation

To publish data to the broker from your own sensor, you'll need to generate an RSA keypair. This can be done by using the included `gen_keys.sh` utility. Simply pass the name you'll be using for the `sensorid` field to the script like so:
```bash
./gen_keys.sh sensor1
```

The script will generate a private/public keypair in `broker/keys`. This can be directly used by the broker if you're running it locally, but in order to update the broker at `n4abi.com`, you'll need to email me (Michael) the public key so I can install it on the server.

# Note to other CPE-4020 groups

Please don't cheat. If you're struggling with your project, please email me, I'll be happy to help.
