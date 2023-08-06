import datetime
from pelops.logging.mylogger import get_child


class AProgram:
    """
    Abstract mode - a mode defines the current behavior of the thermostat.

    yaml config:
        name: Name  # name for this mode
        type: program  # ["program", "schedule"] - needed for mode factory.
    """

    _config = None  # config yaml structure
    _logger = None  # logger instance
    _mqtt_client = None  # mqtt_client instance

    _mqtt_message = None  # img converted to bytes for mqtt transport
    _topic_pub_schedule_image = None  # publish schedule image to this topic
    _topic_pub_program = None

    name = None  # name of this program
    current_setpoint = None

    def __init__(self, config, config_topics_pub, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance - a child will be spawned with the name defined in the config
        """

        self._config = config
        self._mqtt_client = mqtt_client
        self.name = self._config["name"]
        self._logger = get_child(logger, self.name)

        self._logger.info("{}.__init__ - initializing".format(self.name))
        self._logger.debug("{}.__init__ - config: '{}'.".format(self.name, self._config))
        self._topic_pub_schedule_image = config_topics_pub["schedule-image"]
        self._topic_pub_program = config_topics_pub["program-name"]
        self._mqtt_message = ""

    def get_setpoint_at_time(self, time):
        """
        Get the corresponding mode for any time during a day. Will return the same value for the same time on two
        different days.

        :param time: request time as datetime.time instance
        :return: mode instance from schedule
        """
        raise NotImplementedError

    def _publish(self):
        """
        Send the schedule image to a nikippe.mqttimage microservice.
        """
        self._logger.info("ModeSchedule.publish - sending schedule image")

        self._logger.debug("ModeSchedule.publish - mqtt_message: {}".format(self._mqtt_message))
        self._mqtt_client.publish(self._topic_pub_schedule_image, self._mqtt_message)
        self._mqtt_client.publish(self._topic_pub_program, self.name)
        self.current_setpoint.publish()

    def update(self):
        dt = datetime.datetime.now().time()
        self.current_setpoint = self.get_setpoint_at_time(dt)
        self._publish()

    def _set_mqtt_message(self, message):
        self._mqtt_message = message
