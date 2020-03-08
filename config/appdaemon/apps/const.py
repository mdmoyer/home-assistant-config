import appdaemon.plugins.hass.hassapi as hass
import datetime

class Const(hass.Hass):

    HOUSE_MODE_HOME = "Home"
    HOUSE_MODE_ASLEEP = "Asleep"
    HOUSE_MODE_AWAY = "Away"

    PERSON_HOME = "Home"
    PERSON_AWAY = "Away"

    TEMP_REG_NORMAL = "Normal"
    TEMP_REG_NIGHTTIME = "Nighttime"


    def initialize(self):
        pass
