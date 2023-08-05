import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from argaeus.controller.modes.setpoint import SetPoint
from argaeus.controller.modes.programschedule import ProgramSchedule
import collections
import datetime
import threading
from io import BytesIO
from PIL import Image


class Test_ProgramSchedule(unittest.TestCase):
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
        set_point_base = {
            "name": "",
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

        img_config = {
            "width": 192,
            "height": 2,
            "foreground-color": 255,
            "background-color": 100,
            "patterns": {
                "A": 0,
                "B": 1,
                "C": 2,
                "D": 3
            }
        }

        set_point_names = ["A", "B", "C", "D"]

        self.set_points = {}
        set_points_config = []
        for name in set_point_names:
            set_point_base["name"] = name
            mp = SetPoint(set_point_base, self.topics_pub_config, self.mqtt_client, self.logger)
            self.set_points[name] = mp
            set_points_config.append(set_point_base.copy())

        schedule_config = collections.OrderedDict()
        counter = 0
        for hour in range(24):
            for minute in range(0, 60, 15):
                name = "{:02d}:{:02d}".format(hour, minute)
                if counter < 96/4:
                    schedule_config[name] = self.set_points["A"].name
                elif counter < 96/2:
                    schedule_config[name] = self.set_points["B"].name
                elif counter < 96/4*3:
                    schedule_config[name] = self.set_points["C"].name
                else:
                    schedule_config[name] = self.set_points["D"].name
                counter += 1

        self.program_schedule_config = {
            "name": "S",
            "type": "schedule",
            "selectable": True,
            "image": img_config,
            "schedule": schedule_config
        }

    def test_0init(self):
        ms = ProgramSchedule(self.program_schedule_config, self.topics_pub_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(ms)
        self.assertEqual(ms._topic_pub_schedule_image, self.topics_pub_config["schedule-image"])
        self.assertEqual(ms._topic_pub_program, self.topics_pub_config["program-name"])
        self.assertEqual(len(ms.schedule), 0)
        self.assertEqual(len(ms.schedule_raw), 96)

        for k, value in ms.schedule_raw.items():
            key = "{:02d}:{:02d}".format(k.hour, k.minute)
            self.assertEqual(self.program_schedule_config["schedule"][key], value)

        self.assertEqual(ms.name, "S")
        self.assertIsNone(ms.img)

    def test_1sort_dict(self):
        sr_source = self.program_schedule_config["schedule"].copy()
        self.assertEqual(len(sr_source), 96)

        # reverse order of entries
        sr_reverse = {}
        while len(sr_source) > 0:
            key, value = sr_source.popitem()
            sr_reverse[key] = value
        self.assertEqual(len(sr_reverse), 96)

        # check that order of entries is in fact reversed
        sr = self.program_schedule_config["schedule"].copy()
        self.assertEqual(type(sr), collections.OrderedDict)
        self.assertEqual(type(sr_reverse), dict)
        self.assertNotEqual(list(sr.keys())[0], list(sr_reverse.keys())[0])
        self.assertNotEqual(list(sr.keys())[95], list(sr_reverse.keys())[95])
        self.assertEqual(list(sr.keys())[0], list(sr_reverse.keys())[95])
        self.assertEqual(list(sr.keys())[95], list(sr_reverse.keys())[0])

        # get ordered dict
        sr_target = ProgramSchedule._sort_dict(sr_reverse)
        self.assertEqual(len(sr_target), 96)

        # check that order of entries is in fact ordered
        sr = self.program_schedule_config["schedule"].copy()
        self.assertEqual(type(sr), collections.OrderedDict)
        self.assertEqual(type(sr_target), collections.OrderedDict)

        prev_key = None
        for key, value in sr_target.items():
            if prev_key is not None:
                self.assertTrue(prev_key<key)
            prev_key = key

    def test_2map(self):
        ms = ProgramSchedule(self.program_schedule_config, self.topics_pub_config, self.mqtt_client, self.logger)
        self.assertIsNotNone(ms)
        self.assertEqual(len(ms.schedule), 0)
        ms.map_schedule_setpoints(self.set_points)
        self.assertEqual(len(ms.schedule), 96)
        self.assertIsNotNone(ms.img)

        for k,value in ms.schedule.items():
            key = "{:02d}:{:02d}".format(k.hour, k.minute)
            self.assertEqual(self.program_schedule_config["schedule"][key], value.name)
            self.assertIn(value, self.set_points.values())

    def test_3get_set_point_at_time(self):
        ms = ProgramSchedule(self.program_schedule_config, self.topics_pub_config, self.mqtt_client, self.logger)
        ms.map_schedule_setpoints(self.set_points)

        counter = 0
        max_counter = 24*60
        for hour in range(24):
            for minute in range(60):
                key = datetime.time(hour=hour, minute=minute)
                set_point = ms.get_setpoint_at_time(key)
                if counter < max_counter/4:
                    self.assertEqual(set_point, self.set_points["A"])
                elif counter < max_counter/2:
                    self.assertEqual(set_point, self.set_points["B"])
                elif counter < max_counter/4*3:
                    self.assertEqual(set_point, self.set_points["C"])
                else:
                    self.assertEqual(set_point, self.set_points["D"])
                counter += 1

    def test_4mqtt(self):
        on_image_event = threading.Event()
        on_image_event.clear()

        on_name_event = threading.Event()
        on_name_event.clear()

        def _on_name_message(value):
            value = value.decode("UTF-8")
            self.assertEqual(value, "S")
            on_name_event.set()

        def _on_image_message(value):
            try:
                os.mkdir("programschedule")
            except FileExistsError:
                pass

            mqtt_image = Image.open(BytesIO(value))
            mqtt_image = mqtt_image.convert("L")

            self.assertEqual(mqtt_image.size[0], 192)
            self.assertEqual(mqtt_image.size[1], 2)

            mqtt_image.save("programschedule/programschedule_0.png")
            on_image_event.set()

        self.mqtt_client.subscribe(self.topics_pub_config["schedule-image"], _on_image_message)
        self.mqtt_client.subscribe(self.topics_pub_config["program-name"], _on_name_message)

        ms = ProgramSchedule(self.program_schedule_config, self.topics_pub_config, self.mqtt_client, self.logger)
        with self.assertRaises(RuntimeError):
            ms.publish()
        ms.map_schedule_setpoints(self.set_points)

        ms.publish()

        on_image_event.wait(0.5)
        on_name_event.wait(1)
        self.assertTrue(on_image_event.is_set())
        self.assertTrue(on_name_event.is_set())


if __name__ == '__main__':
    unittest.main()
