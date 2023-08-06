from argaeus.controller.modes.modefactory import ModeFactory
from argaeus.controller.acontroller import AController


class ModeController(AController):
    """
    The core controller for the gui - it provides the current mode, program, and schedule:
      * current mode - either a program or a schedule. can be changed via GUI interaction
      * current program - if current mode is a program, then current program equals current mode. otherwise, the program
      that is currently active in the schedule defined by current mode is used as current program
      * current schedule - if current mode is of type ModeSchedule, current schedule is the raw schedule from current
      mode. 'None' oterwise.

    It registers to three topics:
      * prev - select the previous entry in the list of selectable modes as current mode
      * next - select the next entry in the list of selectable modes as current mode
      * default - select the default mode from config as current mode

    After each update, the current schedule chart (or None if no schedule is active) is published.

    config yaml entries:
        default-mode: Schedule  # default mode - must be a name from modes list
        topics-sub:  # incoming topics
            to-prev: /test/r2/rotate  # select previous mode
            command-prev: LEFT  # to previous command - if this value is published to to-prev, the previous entry in the mode list is selected
            to-next: /test/r2/rotate  # select next mode
            command-next: RIGHT  # to next command - if this value is published to to-next, the next entry in the mode list is selected
            to-default: /test/r1/button/pressed  # incoming event to reset to default mode (optional together with command-default)
            command-default: PRESSED  # command for topic-sub / reset to default mode (optional together with to-default)
        topics-pub:  # outgoing topics
            display-server-schedule-image: /test/display/schedule  # topic of an nikippe-mqttimage instance
            display-server-mode: /test/display/mode  # topic of an nikippe-imagelist instance
            temperature-set-point: /test/temperature/set-point  # topic of e.g. epidaurus (=pid temperature control) set-point listener
        modes:  # list of modes
            - name: Night  # unique name for mode entry
              type: program  # program or schedule - a schedule consists of programms
              selectable: True  # can be selected using the gui
              set-point: 19.5  # target temperature of this mode

            - name: Day  # unique name for mode entry
              type: program  # program or schedule - a schedule consists of programms
              selectable: True  # can be selected using the gui
              set-point: 23.0  # target temperature of this mode

            - ...
    """

    _setpoints = None  # dict of modes with mode.name as key - result from ModeFactory
    _programs = None
    _selected_pos = None  # position of currently selected mode
    _default_program = None

    _topic_sub_prev = None  # select previous mode
    _command_prev = None  # command expected on _topic_sub_prev
    _topic_sub_next = None  # select next mode
    _command_next = None  # command expected on _topic_sub_next
    _topic_sub_to_default = None  # reset to default mode - can be None
    _command_default = None  # command expected on _topic_sub_to_default - can be None

    current_program = None  # current program

    def __init__(self, config, mqtt_client, logger):
        """
        Constructor

        :param config: config yaml structure
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance - a child instance will be spawned with name=__name__
        """
        AController.__init__(self, config, mqtt_client, logger, logger_name=__name__)

        self._setpoints, self._programs = ModeFactory.create_modes(self._config["modes"],
                                                                       self._config["topics-pub"], mqtt_client, logger)

        for program in self._programs:
            if program.name == self._config["default-mode"]:
                self._default_program = program
                break
        if self._default_program is None:
            raise KeyError("ModeController.__init__ - unknown value '{}' for default-mode.".
                           format(self._config["default-mode"]))
        self._activate_default_program()

        self._topic_sub_prev = self._config["topics-sub"]["to-prev"]
        self._command_prev = self._config["topics-sub"]["command-prev"]
        self._topic_sub_next = self._config["topics-sub"]["to-next"]
        self._command_next = self._config["topics-sub"]["command-next"]

        try:
            self._topic_sub_to_default = self._config["topics-sub"]["to-default"]
        except KeyError:
            pass

        if self._topic_sub_to_default is not None:
            try:
                self._command_default = self._config["topics-sub"]["command-default"]
            except KeyError:
                self._logger.error("ModeController.__init__ - 'to-default' is set but 'command-default' "
                                   "is missing.")
                raise KeyError("ModeController.__init__ - 'to-default' is set but 'command-default' "
                               "is missing.")

        self._logger.info("ModeController.__init__ - done")

    def _activate_default_program(self):
        """
        Set current mode/program/schedule to the default mode specified in config
        """

        self._logger.info("ModeController._activate_default_mode")
        self._selected_pos = self._programs.index(self._default_program)
        self.current_program = self._default_program
        self.current_program.update()

    def _to_default_handler(self, value):
        """
        Check if the incoming message on _topic_sub_to_default is equivalent to _topic_sub_to_default. Activate
        default mode if yes.

        :param value: mqtt message
        """
        if len(value) > 0 and value.decode("UTF-8") == self._command_default:
            self._logger.info("ModeController._to_default_handler - activate default mode")
            self._activate_default_program()
            self.update()
        else:
            self._logger.warning("ModeController._to_default_handler - dont know how to handle "
                                 "message '{}'".format(value))

    def _topic_handler_prev(self, value):
        """
        Check if the incoming message on _topic_sub_prev is equivalent to _command_prev. Adapt selectable pos
        accordingly and call post topic handler.

        :param value: mqtt message
        """

        if value.decode("utf-8") == self._command_prev:
            self._logger.info("ModeController._topic_handler - command prev.")
            self._selected_pos = self._selected_pos - 1
            self._post_topic_handler()

    def _topic_handler_next(self, value):
        """
        Check if the incoming message on _topic_sub_next is equivalent to _command_next. Adapt selectable pos
        accordingly and call post topic handler.

        :param value: mqtt message
        """

        if value.decode("utf-8") == self._command_next:
            self._logger.info("ModeController._topic_handler - command next.")
            self._selected_pos = self._selected_pos + 1
            self._post_topic_handler()

    def _post_topic_handler(self):
        """
        Make sure that the selectable pos has a valid value and call update
        """
        self._selected_pos = self._selected_pos % len(self._programs)
        self.current_program = self._programs[self._selected_pos]
        self._logger.info("ModeController._topic_handler - selected mode '{}' at pos '{}'.".
                          format(self.current_program.name, self._selected_pos))
        self.update()

    def update(self):
        """
        fill current program and current schedule according to current mode and publish the program and the mode.
        if mode is not ModeSchedule publish an empty message to _topic_pub_schedule_image.
        """
        self._logger.info("ModeController.update")
        self.current_program.update()

    def start(self):
        """
        Subscribe to prev, next, and default
        """
        self._logger.info("ModeController.start - starting")
        self._mqtt_client.subscribe(self._topic_sub_prev, self._topic_handler_prev)
        self._mqtt_client.subscribe(self._topic_sub_next, self._topic_handler_next)
        if self._topic_sub_to_default is not None:
            self._mqtt_client.subscribe(self._topic_sub_to_default, self._to_default_handler)
        self.update()
        self._logger.info("ModeController.start - started")

    def stop(self):
        """
        Unsubscribe from prev, next, and default
        """
        self._logger.info("ModeController.start - stopping")
        self._mqtt_client.unsubscribe(self._topic_sub_prev, self._topic_handler_prev)
        self._mqtt_client.unsubscribe(self._topic_sub_next, self._topic_handler_next)
        if self._topic_sub_to_default is not None:
            self._mqtt_client.unsubscribe(self._topic_sub_to_default, self._to_default_handler)
        self._logger.info("ModeController.start - stopped")

