import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from argaeus.controller.modes.setpoint import SetPoint
from argaeus.controller.modes.programschedule import ProgramSchedule
from argaeus.controller.modes.programsingle import ProgramSingle
from argaeus.controller.modes.modefactory import ModeFactory
import collections


class Test_ModeFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeFactory")
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
        modes_config = []
        for name in set_point_names:
            set_point_base["name"] = name
            if name == "D":
                set_point_base["selectable"] = False
            else:
                set_point_base["selectable"] = True
            mp = SetPoint(set_point_base, self.topics_pub_config, self.mqtt_client, self.logger)
            self.set_points[name] = mp
            modes_config.append(set_point_base.copy())

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

        self.topics_sub_config = {
            "to-left": "/test/rotate",
            "command-left": "LEFT",
            "to-right": "/test/rotate",
            "command-right": "RIGHT"
        }

        modes_config.append(self.program_schedule_config)

        self.config_base = {
            "default-mode": "S",
            "topics-sub": self.topics_sub_config,
            "topics-pub": self.topics_pub_config,
            "modes": modes_config
        }

    def test_0init(self):
        setpoints, programs = ModeFactory.create_modes(self.config_base["modes"], self.config_base["topics-pub"],
                                                       self.mqtt_client, self.logger)
        self.assertIsNotNone(setpoints)
        self.assertEqual(len(setpoints), 4)

        self.assertIsNotNone(programs)
        self.assertEqual(len(programs), 4)
        for program in programs:
            self.assertNotEqual(program.name, "D")
            self.assertNotEqual(program.name, "d")

        self.assertListEqual(list(setpoints.keys()), ["A", "B", "C", "D"])
        self.assertEqual(type(programs[0]), ProgramSingle)
        self.assertEqual(type(programs[1]), ProgramSingle)
        self.assertEqual(type(programs[2]), ProgramSingle)
        self.assertEqual(type(programs[3]), ProgramSchedule)
        self.assertEqual(programs[0].name, "A")
        self.assertEqual(programs[1].name, "B")
        self.assertEqual(programs[2].name, "C")
        self.assertEqual(programs[3].name, "S")

        self.assertEqual(type(programs[3]), ProgramSchedule)
        self.assertEqual(len(programs[3].schedule_raw), 96)
        self.assertEqual(len(programs[3].schedule), 96)
        self.assertIsNotNone(programs[3].img)


if __name__ == '__main__':
    unittest.main()
