import jwt
import requests
import os
import Adafruit_BBIO.GPIO as GPIO

from client.keys import Keys

# setup connection
port = 9000
host = '192.168.1.3'

# define sensor
sensorname = "button"
GPIO.setup("P8_12", GPIO.IN)  # button connects pin 3(3.3v) to pin
# 8.12. A pull down resistor connects to pin 12 and 8.1(GND)
pressValue = "not_pressed"

# create keys
keys = Keys()
keys.load_private_key(sensorname, '../keys/%s_priv.pem' % sensorname)


while True:

    if GPIO.input("P8_14"):
        pressValue = "not_pressed"
    else:
        pressValue = "pressed"

    buttonData = {"sensortype": "press", "sensorid": sensorname,
                  "value": pressValue}

    token = jwt.encode(buttonData, keys.get_private_key(sensorname), "RS256")
    print(token)

    url = 'http://{}:{}/api/sensor'.format(host, port)

    resp = requests.post(url, data=token)
