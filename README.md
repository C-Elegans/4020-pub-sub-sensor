# 4020-pub-sub-sensor

## Broker

### Setup/installing dependencies:
Assuming you have a recent(ish) python (>3.6), run the following in your terminal:
```bash
cd broker
source init_env.sh
```
This should create a virtual python environment, install the dependencies needed for this program, and install a development version of this program.

To run, you can then do the following:
```bash
python -m broker.main
```

Tests can be run by navigating to `broker/tests` and running any of
the python files in there.

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

Keys are generated using `openssl` (you might also be able to generate them with `ssh-keygen` but I'm not sure). To generate a keypair, install openssl then do the following:

```bash
openssl genrsa -out id_priv.pem 2048  # replace id with the sensor id
openssl rsa -in id_priv -outform PEM -pubout -out id_pub.pem
```
(replace id with whatever you'll be using for the sensor id)

You'll then need to put this keypair in the appropriate folder, and/or email me the public key to put on the server. (as to what the appropriate folder is, I don't know yet)

# Note to other CPE-4020 groups

Please don't cheat. If you're struggling with your project, please email me, I'll be happy to help.
