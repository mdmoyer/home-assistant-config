import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class HouseMode(hass.Hass):

    def initialize(self):
        self.const = self.get_app("const")
        self.listen_state(self.log_house_mode_callback, "input_select.house_mode")
        self.listen_state(self.away_mode_activated_callback, "input_select.house_mode", new = "Away")
        self.listen_state(self.away_mode_deactivated_callback, "input_select.house_mode", old = "Away")
        self.listen_state(self.sleep_mode_activated_callback, "input_select.house_mode", new = "Asleep")
        self.listen_state(self.sleep_mode_deactivated_callback, "input_select.house_mode", old = "Asleep")
        self.run_daily(self.wake_up_callback, "07:00:00")
        self.listen_state(self.leave_home_callback, "person.mm", old = "Home", new = "Away")
        self.listen_state(self.leave_home_callback, "person.nl", old = "Home", new = "Away")
        self.listen_state(self.return_home_callback, "person.mm", new = "Home")
        self.listen_state(self.return_home_callback, "person.nl", new = "Home")

    def log_house_mode_callback(self, entity, attribute, old, new, kwargs):
        self.log("House mode: " + old + " --> " + new)

    def away_mode_activated_callback(self, entity, attribute, old, new, kwargs):
        # Set the thermostat to "Eco" mode.
        self.call_service("climate/set_preset_mode", entity_id = "climate.dining_room_nest", preset_mode = "eco")

    def away_mode_deactivated_callback(self, entity, attribute, old, new, kwargs):
        # Turn off "Eco" mode on the thermostat.
        self.call_service("climate/set_preset_mode", entity_id = "climate.dining_room_nest", preset_mode = "none")

    def sleep_mode_activated_callback(self, entity, attribute, old, new, kwargs):
        # Turn off all lights in the house.
        self.call_service("light/turn_off", entity_id = "all")
        # Set temperature regulation to nighttime mode.
        self.select_option("input_select.temp_reg", const.TEMP_REG_NIGHTTIME)

    def sleep_mode_deactivated_callback(self, entity, attribute, old, new, kwargs):
        # Return temperature regulation to normal.
        self.select_option("input_select.temp_reg", const.TEMP_REG_NORMAL)

    def leave_home_callback(self, entity, attribute, old, new, kwargs):
        # Change house_mode to Away if everyone is away.
        if self.get_state("person.mm") == const.PERSON_AWAY and self.get_state("person.nl") == const.PERSON_AWAY:
            self.select_option("input_select.house_mode", const.HOUSE_MODE_AWAY)

    def return_home_callback(self, entity, attribute, old, new, kwargs):
        # Change house_mode to Home if someone comes home and the house is in Away mode.
        if self.get_state("input_select.house_mode") == const.HOUSE_MODE_AWAY:
            self.select_option("input_select.house_mode", const.HOUSE_MODE_HOME)

    def wake_up_callback(self, kwargs):
        # Change house_mode to Home only if it is currently set to Asleep
        if self.get_state("input_select.house_mode") == const.HOUSE_MODE_ASLEEP:
            self.select_option("input_select.house_mode", const.HOUSE_MODE_HOME)
