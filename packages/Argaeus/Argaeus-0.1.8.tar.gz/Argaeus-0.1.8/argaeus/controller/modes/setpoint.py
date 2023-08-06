from pelops.logging.mylogger import get_child


class SetPoint:
    """
    A setpoint sets the current temperature. It can either be selected via GUI or activated via a mode schedule.

    yaml config entry:
        name: Name  # name for this mode
        selectable: True  # True/False - if set to False it cannot be selected via GUI
        type: program  # ["program", "schedule"] - needed for mode factory.
        set-point: 19.5  # target temperature of this mode
    """

    _config = None  # config yaml structure
    _logger = None  # logger instance
    _mqtt_client = None  # mqtt_client instance

    name = None  # name of this mode
    selectable = None  # can this mode be activated via GUI

    set_point = None  # current set_point for temperature
    default_set_point = None  # default set_point for temperature (=value taken from config)
    _topic_pub_temperature = None  # publish topic for set_point
    _topic_pub_name = None  # publish topic for mode_icon

    def __init__(self, config, config_topics_pub, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param config_topics_pub: a dict with all topics that can be published to
        :param mqtt_client: mqtt_client instance
        :param logger: logger instance
        """

        self._config = config
        self._mqtt_client = mqtt_client
        self.name = self._config["name"]
        self._logger = get_child(logger, self.name)

        self._logger.info("{}.__init__ - initializing".format(self.name))
        self._logger.debug("{}.__init__ - config: '{}'.".format(self.name, self._config))

        self.selectable = bool(self._config["selectable"])

        self.set_point = float(self._config["set-point"])
        self.default_set_point = self.set_point
        self._topic_pub_temperature = config_topics_pub["set-point-temperature"]
        self._topic_pub_name = config_topics_pub["set-point-name"]

    def publish(self):
        """Publish set_point and name as mode_icon."""
        self._mqtt_client.publish(self._topic_pub_temperature, self.set_point)
        self._mqtt_client.publish(self._topic_pub_name, self.name.lower())

