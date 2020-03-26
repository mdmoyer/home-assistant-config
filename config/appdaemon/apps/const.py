import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class Const(hass.Hass):

    HOUSE_MODE_HOME = "Home"
    HOUSE_MODE_ASLEEP = "Asleep"
    HOUSE_MODE_AWAY = "Away"

    # Person state is "home" or "not_home", or the zone's full name otherwise.
    PERSON_HOME = "home"
    PERSON_AWAY = "not_home"

    TEMP_REG_NORMAL = "Normal"
    TEMP_REG_NIGHTTIME = "Nighttime"

    def initialize(self):
        pass
