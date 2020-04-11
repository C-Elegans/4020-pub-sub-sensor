import jwt
import requests

from broker.keys import Keys

port = 9000
host = 'localhost'

keys = Keys()
keys.enable_example = True
keys.load_example('ex')

exampledata = {"sensortype": "noise",
               "sensorid": "1",
               "value": "-93dB"}

token = jwt.encode(exampledata, keys.get_private_key('ex'), "RS256")
print(token)

url = 'http://{}:{}/api/sensor'.format(host, port)

resp = requests.post(url, data=token)
