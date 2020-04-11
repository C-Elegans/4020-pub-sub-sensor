import json
import jwt
import aiounittest
import asyncio

from broker.main import app, appdata

exampledata = {"sensortype": "noise",
               "sensorid": "1",
               "value": "-93dB"}




class BrokerTests(aiounittest.AsyncTestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        appdata.keys.enable_example = True
        appdata.keys.load_example("1")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        pass

    async def test_index(self):
        resp = await self.app.get('/')
        data = await resp.get_data()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data, b"Hello, World!")

    async def test_update_sensor(self):
        priv_key = appdata.keys.get_private_key("1")
        token = jwt.encode(exampledata, priv_key, 'RS256')
        resp = await self.app.put('/api/sensor', data=token)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('1' in appdata.sensors)
        sensor = appdata.sensors['1']
        self.assertEqual(sensor.name, '1')
        self.assertEqual(sensor.stype, 'noise')
        self.assertEqual(sensor.value, '-93dB')

    async def test_get_sensors(self):
        priv_key = appdata.keys.get_private_key("1")
        token = jwt.encode(exampledata, priv_key, 'RS256')
        resp = await self.app.put('/api/sensor', data=token)
        self.assertEqual(resp.status_code, 200)
        resp = await self.app.get('/api/sensor')
        json = await resp.get_json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(json), 1)
        self.assertDictEqual(json[0], exampledata)
