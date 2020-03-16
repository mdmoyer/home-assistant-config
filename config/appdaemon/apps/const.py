import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class Const(hass.Hass):

    HOUSE_MODE_HOME = "Home"
    HOUSE_MODE_ASLEEP = "Asleep"
    HOUSE_MODE_AWAY = "Away"

    PERSON_HOME = "home"
    PERSON_AWAY = "not_home"

    TEMP_REG_NORMAL = "Normal"
    TEMP_REG_NIGHTTIME = "Nighttime"

    def initialize(self):
        pass
