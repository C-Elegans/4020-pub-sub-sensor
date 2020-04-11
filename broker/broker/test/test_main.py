import unittest
import json
import jwt

from broker.main import app, appdata

exampledata = {"sensortype": "noise",
               "sensorid": "1",
               "value": "-93dB"}

class BrokerTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        appdata.keys.enable_example = True
        appdata.keys.load_example("1")

    def tearDown(self):
        pass

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b"Hello, World!")

    def test_update_sensor(self):
        priv_key = appdata.keys.get_private_key("1")
        token = jwt.encode(exampledata, priv_key, 'RS256')
        resp = self.app.put('/api/sensor', data=token)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('1' in appdata.sensors)
        sensor = appdata.sensors['1']
        self.assertEqual(sensor.name, '1')
        self.assertEqual(sensor.stype, 'noise')
        self.assertEqual(sensor.value, '-93dB')

    def test_get_sensors(self):
        priv_key = appdata.keys.get_private_key("1")
        token = jwt.encode(exampledata, priv_key, 'RS256')
        resp = self.app.put('/api/sensor', data=token)
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/api/sensor')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 1)
        self.assertDictEqual(resp.json[0], exampledata)


if __name__ == '__main__':
    unittest.main()
