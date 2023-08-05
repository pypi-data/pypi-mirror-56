from argaeus.controller.modes.aprogram import AProgram


class ProgramSingle(AProgram):
    _setpoint = None

    def __init__(self, config, config_topics_pub, setpoint, mqtt_client, logger):
        AProgram.__init__(self, config, config_topics_pub, mqtt_client, logger)
        self._setpoint = setpoint

    def get_setpoint_at_time(self, time):
        return self._setpoint

