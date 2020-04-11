# 4020-pub-sub-sensor

## Broker API

### Publishing

To publish a sensor value, submit a HTTP POST request to n4abi.com:9000/api/sensor using a JSON Web token of the following format:

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

### Subscribing

To subscribe to sensor values, you will need to open a raw TCP socket to n4abi.com:9001, and send a json message of the following format:

```json
{cmd: "subscribe", "sensortype": "type", "sensorid": "id"}
```

Note that the `sensortype` and `sensorid` fields are optional. If you'd like to receive messages from all sensors of a given type, just omit the `sensorid` field.

Whenever a sensor publishes some data, you'll receive some JSON data in the following format:
```json
{"sensortype": "type", "sensorid": "id", "value": "value"}
```


# Note to other CPE-4020 groups

Please don't cheat. If you're struggling with your project, please email me, I'll be happy to help. 
