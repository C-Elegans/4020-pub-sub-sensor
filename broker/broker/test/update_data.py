import jwt
import requests

from broker.keys import Keys

port = 9000
host = 'localhost'

keys = Keys()
keys.load_private_key('1', '../keys/1_priv.pem')

exampledata = {"sensortype": "noise",
               "sensorid": "1",
               "value": "-93dB"}

token = jwt.encode(exampledata, keys.get_private_key('1'), "RS256")
print(token)

url = 'http://{}:{}/api/sensor'.format(host, port)

resp = requests.post(url, data=token)
