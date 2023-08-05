import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from argaeus.controller.modes.setpoint import SetPoint
from argaeus.controller.modes.programsingle import ProgramSingle
import collections
import datetime
import threading
from io import BytesIO
from PIL import Image


class Test_ProgramSingle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ProgramSchedule")
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
        self.set_point_config = {
            "name": "A",
            "type": "set-point",
            "selectable": True,
            "set-point": 19.5
        }

        self.topics_pub_config = {
            "program-name": "/test/program",
            "schedule-image": "/test/schedule",
            "set-point-name": "/test/setpoint/name",
            "set-point-temperature": "/test/setpoint/temperature"
        }

    def test_0init(self):
        setpoint = SetPoint(self.set_point_config, self.topics_pub_config, self.mqtt_client, self.logger)
        ms = ProgramSingle(self.set_point_config, self.topics_pub_config, setpoint, self.mqtt_client, self.logger)
        self.assertIsNotNone(ms)
        self.assertIsNotNone(setpoint)
        self.assertEqual(ms._topic_pub_schedule_image, self.topics_pub_config["schedule-image"])
        self.assertEqual(ms.name, "A")

    def test_1get_set_point_at_time(self):
        setpoint = SetPoint(self.set_point_config, self.topics_pub_config, self.mqtt_client, self.logger)
        ms = ProgramSingle(self.set_point_config, self.topics_pub_config, setpoint, self.mqtt_client, self.logger)

        for hour in range(24):
            for minute in range(60):
                key = datetime.time(hour=hour, minute=minute)
                program = ms.get_setpoint_at_time(key)
                self.assertEqual(program, setpoint)

    def test_2mqtt(self):
        on_image_event = threading.Event()
        on_image_event.clear()

        on_name_event = threading.Event()
        on_name_event.clear()

        def _on_name_message(value):
            value = value.decode("UTF-8")
            self.assertEqual(value, "A")
            on_name_event.set()

        def _on_image_message(value):
            value = value.decode("UTF-8")
            self.assertEqual(value, "")
            on_image_event.set()

        self.mqtt_client.subscribe(self.topics_pub_config["schedule-image"], _on_image_message)
        self.mqtt_client.subscribe(self.topics_pub_config["program-name"], _on_name_message)

        setpoint = SetPoint(self.set_point_config, self.topics_pub_config, self.mqtt_client, self.logger)
        ms = ProgramSingle(self.set_point_config, self.topics_pub_config, setpoint, self.mqtt_client, self.logger)
        ms.publish()
        on_image_event.wait(0.5)
        on_name_event.wait(1)
        self.assertTrue(on_image_event.is_set())
        self.assertTrue(on_name_event.is_set())


if __name__ == '__main__':
    unittest.main()
