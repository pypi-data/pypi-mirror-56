import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
import threading
from argaeus.controller.modes.setpoint import SetPoint


class Test_ModeProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeProgram")
        cls.logger.info("start")
        cls.mqtt_client = MyMQTTClient(cls.config["mqtt"], cls.logger)
        cls.mqtt_client.connect()

    @classmethod
    def tearDownClass(cls):
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def tearDown(self):
        self.mqtt_client.unsubscribe_all()

    def setUp(self):
        self.mode_config = {
            "name": "Night",
            "type": "set-point",
            "selectable": True,
            "set-point": 19.5
        }

        self.topics_pub_config = {
            "set-point-name": "/test/setpoint/name",
            "set-point-temperature": "/test/setpoint/temperature"
            }

    def test_0init(self):
        mp = SetPoint(self.mode_config, self.topics_pub_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(mp)
        self.assertEqual(mp.name, "Night")
        self.assertEqual(mp.selectable, True)
        self.assertEqual(mp.set_point, 19.5)
        self.assertEqual(mp.default_set_point, 19.5)
        self.assertEqual(mp._topic_pub_name, "/test/setpoint/name")
        self.assertEqual(mp._topic_pub_temperature, "/test/setpoint/temperature")

    def test_1mqtt(self):
        global setpoint_name_event
        setpoint_name_event = threading.Event()
        setpoint_name_event.clear()
        global setpoint_temperature_event
        setpoint_temperature_event = threading.Event()
        setpoint_temperature_event.clear()

        def setpoint_temperature(value):
            self.assertEqual(float(value), 19.5)
            setpoint_temperature_event.set()

        def setpoint_name(value):
            value = value.decode("UTF-8")
            self.assertEqual(value, "Night".lower())
            setpoint_name_event.set()

        self.mqtt_client.subscribe("/test/setpoint/name", setpoint_name)
        self.mqtt_client.subscribe("/test/setpoint/temperature", setpoint_temperature)

        mp = SetPoint(self.mode_config, self.topics_pub_config, self.mqtt_client, self.logger)
        mp.publish()

        setpoint_name_event.wait(0.5)
        setpoint_temperature_event.wait(0.5)

        self.assertEqual(setpoint_name_event.is_set(), True)
        self.assertEqual(setpoint_temperature_event.is_set(), True)


if __name__ == '__main__':
    unittest.main()
