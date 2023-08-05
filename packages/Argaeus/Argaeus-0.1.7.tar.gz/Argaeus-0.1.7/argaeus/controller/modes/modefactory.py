from argaeus.controller.modes.setpoint import SetPoint
from argaeus.controller.modes.programschedule import ProgramSchedule
from argaeus.controller.modes.programsingle import ProgramSingle
from pelops.logging.mylogger import get_child


class ModeFactory:
    """
    Generation of mode instances
    """

    @staticmethod
    def create_modes(config, config_topics_pub, mqtt_client, logger):
        """
        Takes a list of mode config entries and returns a list of mode instances. Schedules are already properly
        initialized (cp. two step initialization of ModeSchedule.

        :param config: config yaml structure
        :param config_topics_pub:  a dict with all topics that can be published to
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance
        :return: modes (dict with all generated instances - keys are mode.name), modes_selectable (a list with all all
        generated instances that can be selected via gui)
        """

        log = get_child(logger, __name__)
        log.info("ModeFactory.create_modes - creating modes ('{}').".format(config))

        setpoints = {}
        programs = []
        for c in config:
            t = c["type"].lower()
            if t == "set-point":
                setpoint = SetPoint(c, config_topics_pub, mqtt_client, logger)
                setpoints[setpoint.name] = setpoint
                if setpoint.selectable:
                    programs.append(ProgramSingle(c, config_topics_pub, setpoint, mqtt_client, logger))
            elif t == "schedule":
                if c["selectable"]:
                    schedule = ProgramSchedule(c, config_topics_pub, mqtt_client, logger)
                    programs.append(schedule)

        log.info("ModeFactory.create_modes - map_schedule_modes")
        for program in programs:
            if isinstance(program, ProgramSchedule):
                program.map_schedule_setpoints(setpoints)

        return setpoints, programs
