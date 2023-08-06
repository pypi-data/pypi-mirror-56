import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from argaeus.controller.modes.modecontroller import ModeController
from PIL import Image, ImageChops
from io import BytesIO
import time, datetime
import math
import threading


class Test_ModeController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ModeController")
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
        self._wait()

    def _wait(self, minimum_seconds_to_next_minute=5):
        # guarantee that we will not have a racing condidtion like timestamp init is "00:14:59" and timestmap
        # assertion is "00:15:01" which could result in different schedule entries being used.
        wait = (60 - time.time() % 60) + 0.1
        if wait > minimum_seconds_to_next_minute:
            wait = 0  # everything is fine
        elif wait > 1:
            print("... waiting {} seconds before test starts.".format(wait))
        else:
            pass # wait time is short enough - no need to bother user
        time.sleep(wait)

    @staticmethod
    def _equal(im1, im2):
        return ImageChops.difference(im1, im2).getbbox() is None

    def test_0init(self):
        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        self.assertEqual(len(mc._setpoints), 4)
        self.assertEqual(len(mc._programs), 4)
        self.assertEqual(mc.current_program.name, "Schedule")
        self.assertEqual(len(mc.current_program.schedule), 96)

        now = datetime.datetime.now().time()
        pos = math.floor(datetime.timedelta(hours=now.hour, minutes=now.minute) / datetime.timedelta(minutes=15))
        current_setpoint = list(mc.current_program.schedule.values())[pos]
        self.assertEqual(mc.current_program.current_setpoint.name, current_setpoint.name)

        self.assertEqual(mc._topic_sub_prev, self.config["controller"]["mode-controller"]["topics-sub"]["to-prev"])
        self.assertEqual(mc._command_prev, self.config["controller"]["mode-controller"]["topics-sub"]["command-prev"])
        self.assertEqual(mc._topic_sub_next, self.config["controller"]["mode-controller"]["topics-sub"]["to-next"])
        self.assertEqual(mc._command_next, self.config["controller"]["mode-controller"]["topics-sub"]["command-next"])
        self.assertEqual(mc.current_program._topic_pub_schedule_image,
                         self.config["controller"]["mode-controller"]["topics-pub"]["schedule-image"])
        self.assertEqual(mc.current_program._topic_pub_program,
                         self.config["controller"]["mode-controller"]["topics-pub"]["program-name"])
        self.assertEqual(mc._topic_sub_to_default,
                         self.config["controller"]["mode-controller"]["topics-sub"]["to-default"])
        self.assertEqual(mc._command_default,
                         self.config["controller"]["mode-controller"]["topics-sub"]["command-default"])

    def test_1start_stop(self):
        hsi = threading.Event()
        hsi.clear()
        hspn = threading.Event()
        hspn.clear()
        hspt = threading.Event()
        hspt.clear()
        hpn = threading.Event()
        hpn.clear()

        def _handler_program_name(value):
            self.assertEqual(value.decode("UTF-8").lower(), mc.current_program.name.lower())
            hpn.set()

        def _handler_schedule_image(value):
            self.assertTrue(len(value)>0)
            mqtt_image = Image.open(BytesIO(value))
            mqtt_image = mqtt_image.convert("L")
            Test_ModeController._equal(mqtt_image, mc.current_program.img)
            hsi.set()

        def _handler_set_point_name(value):
            self.assertEqual(value.decode("UTF-8").lower(), mc.current_program.current_setpoint.name.lower())
            hspn.set()

        def _handler_set_point_temperature(value):
            self.assertEqual(float(value), mc.current_program.current_setpoint.set_point)
            hspt.set()

        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["schedule-image"],
            _handler_schedule_image)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["program-name"],
            _handler_program_name)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["set-point-name"],
            _handler_set_point_name)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["set-point-temperature"],
            _handler_set_point_temperature)

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        mc.start()

        hsi.wait(1)
        hspt.wait(1)
        hspn.wait(1)
        hpn.wait(1)

        self.assertTrue(hsi.is_set())
        self.assertTrue(hspt.is_set())
        self.assertTrue(hspn.is_set())
        self.assertTrue(hpn.is_set())

        mc.stop()

    def test_2prev_next(self):
        self._wait()

        def _clear_all():
            hspn.clear()
            hsi.clear()
            hspt.clear()
            hpn.clear()

        def _wait_all():
            hsi.wait(2)
            hspt.wait(2)
            hspn.wait(2)
            hpn.wait(2)

            self.assertTrue(hsi.is_set())
           # print("hsi")
            self.assertTrue(hspt.is_set())
           # print("hspt")
            self.assertTrue(hspn.is_set())
           # print("hspn")
            self.assertTrue(hpn.is_set())
           # print("hpn")
           # print("_wait_all finsihed")

        hsi = threading.Event()
        hspn = threading.Event()
        hspt = threading.Event()
        hpn = threading.Event()

        _clear_all()

        schedule_images = []
        program_names = []
        set_point_names = []
        set_point_temperature = []

        def _handler_schedule_image(value):
            if len(value)>0:
                mqtt_image = Image.open(BytesIO(value))
                mqtt_image = mqtt_image.convert("L")
                self.assertIsNotNone(mqtt_image)
                schedule_images.append(mqtt_image)
            else:
                schedule_images.append(None)
            hsi.set()

        def _handler_set_point_name(value):
            self.assertEqual(value.decode("UTF-8").lower(), mc.current_program.current_setpoint.name.lower())
            set_point_names.append(value.decode("UTF-8").lower())
            hspn.set()

        def _handler_set_point_temperature(value):
            self.assertEqual(float(value), mc.current_program.current_setpoint.set_point)
            set_point_temperature.append(float(value))
            hspt.set()

        def _handler_program_name(value):
            self.assertEqual(value.decode("UTF-8").lower(), mc.current_program.name.lower())
            program_names.append(value.decode("UTF-8").lower())
            hpn.set()

        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["schedule-image"],
            _handler_schedule_image)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["program-name"],
            _handler_program_name)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["set-point-name"],
            _handler_set_point_name)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["set-point-temperature"],
            _handler_set_point_temperature)

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)

        default_program = mc.current_program.name.lower()
        default_setpoint_temperature = mc.current_program.current_setpoint.set_point
        default_setpoint_name = mc.current_program.current_setpoint.name.lower()

        mc.start()
        time.sleep(0.5)  # necessary wait - otherwise racing conditions might happen
        _wait_all()
        _clear_all()

        # turn counter-clockwise
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()

        # turn clockwise
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()
        self.mqtt_client.publish(mc._topic_sub_next, mc._command_next)
        _wait_all()
        _clear_all()

        mc.stop()

        # the first value (defaults) must appear two times - this is due to mqtt mode 2 (sends last value upon sub)
        expected_program_names = [default_program, default_program, 'morning', 'day', 'night', default_program, 'night',
                                  'day', 'morning', default_program]
        expected_set_point_names = [default_setpoint_name, default_setpoint_name, 'morning', 'day', 'night',
                                    default_setpoint_name, 'night', 'day', 'morning', default_setpoint_name]
        expected_set_point_temperatures = [default_setpoint_temperature, default_setpoint_temperature, 21.5, 23.0, 19.5,
                                           default_setpoint_temperature, 19.5, 23.0, 21.5, default_setpoint_temperature]
        self.assertListEqual(program_names, expected_program_names)
        self.assertListEqual(set_point_names, expected_set_point_names)
        self.assertListEqual(set_point_temperature, expected_set_point_temperatures)

        self.assertIsNotNone(schedule_images[0])
        self.assertIsNotNone(schedule_images[1])
        self.assertIsNone(schedule_images[2])
        self.assertIsNone(schedule_images[3])
        self.assertIsNone(schedule_images[4])
        self.assertIsNotNone(schedule_images[5])
        self.assertIsNone(schedule_images[6])
        self.assertIsNone(schedule_images[7])
        self.assertIsNone(schedule_images[8])
        self.assertIsNotNone(schedule_images[9])

    def test_3to_default_mode(self):
        self._wait()

        def _clear_all():
            hspn.clear()
            hsi.clear()
            hspt.clear()
            hspn.clear()

        def _wait_all():
            hsi.wait(1)
            hspt.wait(1)
            hspn.wait(1)
            hpn.wait(1)

            self.assertTrue(hsi.is_set())
            self.assertTrue(hspt.is_set())
            self.assertTrue(hspn.is_set())
            self.assertTrue(hpn.is_set())

        hsi = threading.Event()
        hspn = threading.Event()
        hspt = threading.Event()
        hpn = threading.Event()

        _clear_all()

        def _handler_schedule_image(value):
            hsi.set()

        def _handler_set_point_name(value):
            hspn.set()

        def _handler_set_point_temperature(value):
            hspt.set()

        def _handler_program_name(value):
            hpn.set()

        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["schedule-image"],
            _handler_schedule_image)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["program-name"],
            _handler_program_name)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["set-point-name"],
            _handler_set_point_name)
        self.mqtt_client.subscribe(
            self.config["controller"]["mode-controller"]["topics-pub"]["set-point-temperature"],
            _handler_set_point_temperature)

        mc = ModeController(self.config["controller"]["mode-controller"], self.mqtt_client, self.logger)
        self.assertIsNotNone(mc)
        default_program = mc.current_program.name.lower()
        default_setpoint_name = mc.current_program.current_setpoint.name.lower()

        mc.start()
        time.sleep(1)
        _wait_all()
        _clear_all()

        # turn counter-clockwise
        self.mqtt_client.publish(mc._topic_sub_prev, mc._command_prev)
        _wait_all()
        _clear_all()
        self.assertNotEqual(default_program, mc.current_program.name.lower())
        self.assertNotEqual(default_setpoint_name, mc.current_program.current_setpoint.name.lower())

        self.mqtt_client.publish(self.config["controller"]["mode-controller"]["topics-sub"]["to-default"],
                                 self.config["controller"]["mode-controller"]["topics-sub"]["command-default"])
        _wait_all()
        _clear_all()

        self.assertEqual(default_program, mc.current_program.name.lower())
        self.assertEqual(default_setpoint_name, mc.current_program.current_setpoint.name.lower())

        mc.stop()


if __name__ == '__main__':
    unittest.main()
