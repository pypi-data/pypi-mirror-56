import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.logging.mylogger import create_logger
from pelops.mymqttclient import MyMQTTClient
from pelops.myconfigtools import read_config
from argaeus.thermostatguicontroller import ThermostatGUIController
import time
import threading


class Test_ThermostatGUIController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "Test_ThermostatGUIController")
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
            pass  # wait time is short enough - no need to bother user
        time.sleep(wait)

    def test_0init(self):
        tgc = ThermostatGUIController(self.config, self.mqtt_client, self.logger)
        self.assertIsNotNone(tgc)
        self.assertIsNotNone(tgc._operation_controller)
        self.assertIsNotNone(tgc._set_point_controller)
        self.assertIsNotNone(tgc._mode_controller)

    def test_1start_stop(self):
        self._wait(10)

        hsi = threading.Event()
        hspn = threading.Event()
        hspt = threading.Event()
        hpn = threading.Event()
        ch = threading.Event()

        hsi.clear()
        hspn.clear()
        hspt.clear()
        hpn.clear()
        ch.clear()

        def _handler_schedule_image(value):
            hsi.set()

        def _handler_program_name(value):
            hpn.set()

        def _handler_set_point_name(value):
            hspn.set()

        def _handler_set_point_temperature(value):
            hspt.set()

        def _command_handler(value):
            ch.set()

        self.mqtt_client.subscribe(self.config["controller"]["operation-controller"]["topic-pub"], _command_handler)

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

        tgc = ThermostatGUIController(self.config, self.mqtt_client, self.logger, no_gui=True)
        tgc.start()

        hsi.wait(1)
        hspn.wait(1)
        hspt.wait(1)
        hpn.wait(1)
        ch.wait(1)

        self.assertTrue(hsi.is_set())
        self.assertTrue(hspn.is_set())
        self.assertTrue(hspt.is_set())
        self.assertTrue(hpn.is_set())
        self.assertTrue(ch.is_set())

        t = time.time()
        tgc.stop()
        diff = time.time() - t
        self.assertLess(diff, 2)  # stopping should be relatively fast - faster than the next poll intervall at least

    def test_2_mulitple_events(self):
        self._wait(10)

        hsi = threading.Event()
        hspn = threading.Event()
        hspt = threading.Event()
        hpn = threading.Event()

        def _clear_all():
            hspn.clear()
            hsi.clear()
            hspt.clear()
            hpn.clear()

        def _wait_all(timeout=1):
            hsi.wait(timeout)
            hspt.wait(timeout)
            hspn.wait(timeout)
            hpn.wait(timeout)

            self.assertTrue(hsi.is_set())
            self.assertTrue(hspt.is_set())
            self.assertTrue(hspn.is_set())
            self.assertTrue(hpn.is_set())

        _clear_all()

        def _handler_schedule_image(value):
            hsi.set()

        def _handler_program_name(value):
            hpn.set()

        def _handler_set_point_name(value):
            hspn.set()

        def _handler_set_point_temperature(value):
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

        tgc = ThermostatGUIController(self.config, self.mqtt_client, self.logger, no_gui=True)
        tgc.start()
        start_time = time.time()

        print("waiting for next event (120s maximum)\n")

        _wait_all(65)
        _clear_all()
        _wait_all(65)
        _clear_all()

        wait_time = (60 - start_time) % 60  # seconds to next update loop
        print("waiting for {} seconds for next event.\n".format(wait_time))

        hsi.wait(timeout=wait_time+0.1)  # add safety seconds
        hspn.wait(1)
        hspt.wait(1)
        hpn.wait(1)

        self.assertTrue(hsi.is_set())
        self.assertTrue(hspn.is_set())
        self.assertTrue(hspt.is_set())
        self.assertTrue(hpn.is_set())

        self.assertLess(time.time(), start_time+wait_time+0.1)
        self.assertGreater(time.time(), start_time+wait_time-0.1)

        tgc.stop()


if __name__ == '__main__':
    unittest.main()

