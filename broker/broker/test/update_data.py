import jwt
import requests

from broker.keys import Keys

port = 9000
host = 'localhost'

sensorname = "ex"
keys = Keys()
keys.load_private_key(sensorname, '../keys/ex_priv.pem')

exampledata = {"sensortype": "noise",
               "sensorid": sensorname,
               "value": "-93dB"}

token = jwt.encode(exampledata, keys.get_private_key(sensorname), "RS256")
print(token)

url = 'http://{}:{}/api/sensor'.format(host, port)

resp = requests.post(url, data=token)
