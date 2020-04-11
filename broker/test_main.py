import unittest
import json

from main import app, appdata

class BrokerTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b"Hello, World!")

    def test_update_sensor(self):
        data = {"sensortype": "noise",
                "sensorid": "1",
                "value": "-93dB"}
        resp = self.app.put('/api/sensor', json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('1' in appdata.sensors)
        sensor = appdata.sensors['1']
        self.assertEqual(sensor.name, '1')
        self.assertEqual(sensor.stype, 'noise')
        self.assertEqual(sensor.value, '-93dB')


if __name__ == '__main__':
    unittest.main()
