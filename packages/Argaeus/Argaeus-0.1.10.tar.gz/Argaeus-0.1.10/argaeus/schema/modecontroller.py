import argaeus.schema.modeprogram
import argaeus.schema.modeschedule


def get_schema():
    schema = {
        "mode-controller": {
            "description": "list of different operation modes like fixed temperature or time schedule driven",
            "type": "object",
            "properties": {
                "default-mode": {
                    "description": "default mode - must be a name from modes list",
                    "type": "string"
                },
                "topics-pub": {
                    "description": "outgoing topics",
                    "type": "object",
                    "properties": {
                        "schedule-image": {
                            "description": "topic of an nikippe-mqttimage instance",
                            "type": "string"
                        },
                        "program-name": {
                            "description": "the name of the currently active program. typical values are 'manual' and 'schedule'. see list of schedule entries and additionally 'manual' for directly selected mode. can be used for an nikippe-imagelist instance",
                            "type": "string"
                        },
                        "set-point-name": {
                            "description": "the name of the currently active set-point. typical values are 'day', 'night', 'frost', or 'morning'. see list of modes in config file (except schedule entries). can be used for an nikippe-imagelist instance",
                            "type": "string"
                        },
                        "set-point-temperature": {
                            "description": "topic of e.g. epidaurus (=pid temperature control) set-point listener",
                            "type": "string"
                        },
                    },
                    "required": ["schedule-image", "set-point-name", "program-name", "set-point-temperature"],
                    "additionalItems": False
                },
                "topics-sub": {
                    "description": "incoming topics",
                    "type": "object",
                    "properties": {
                        "to-prev": {
                            "description": "select previous mode",
                            "type": "string"
                        },
                        "command-prev": {
                            "description": "to previous command - if this value is published to to-prev, the previous "
                                           "entry in the mode list is selected",
                            "type": "string"
                        },
                        "to-next": {
                            "description": "select next mode",
                            "type": "string"
                        },
                        "command-next": {
                            "description": "to next command - if this value is published to to-next, the next "
                                           "entry in the mode list is selected",
                            "type": "string"
                        },
                        "to-default": {
                            "description": "incoming event to reset to default mode (optional together with "
                                           "command-default)",
                            "type": "string"
                        },
                        "command-default": {
                            "description": "command for topic-sub / reset to default mode (optional together with "
                                           "to-default)",
                            "type": "string"
                        }
                    },
                    "required": ["to-prev", "command-prev", "to-next", "command-next"],
                    "additionalItems": False
                },
                "modes": {
                    "description": "list of modes",
                    "type": "array",
                    "items": {
                        "anyof": [
                            argaeus.schema.modeschedule.get_schema(),
                            argaeus.schema.modeprogram.get_schema()
                        ]
                    }
                },

            },
            "required": ["default-mode", "topics-sub", "topics-pub", "modes"],
            "additionalProperties": False
        }
    }

    return schema
