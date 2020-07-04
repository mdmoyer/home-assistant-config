import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class HouseMode(hass.Hass):

    def initialize(self):
        self.const = self.get_app("const")
        self.listen_state(self.log_house_mode_callback, "input_select.house_mode")
        self.listen_state(self.away_mode_activated_callback, "input_select.house_mode", new = self.const.HOUSE_MODE_AWAY)
        self.listen_state(self.away_mode_deactivated_callback, "input_select.house_mode", old = self.const.HOUSE_MODE_AWAY)
        self.listen_state(self.sleep_mode_activated_callback, "input_select.house_mode", new = self.const.HOUSE_MODE_ASLEEP)
        self.listen_state(self.sleep_mode_deactivated_callback, "input_select.house_mode", old = self.const.HOUSE_MODE_ASLEEP)
        self.run_daily(self.wake_up_callback, "07:00:00")
        self.listen_state(self.update_home_status_callback, "person")

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
        self.select_option("input_select.temp_reg", self.const.TEMP_REG_NIGHTTIME)

    def sleep_mode_deactivated_callback(self, entity, attribute, old, new, kwargs):
        # Return temperature regulation to normal.
        self.select_option("input_select.temp_reg", self.const.TEMP_REG_NORMAL)

    def update_home_status_callback(self, entity, attribute, old, new, kwargs):
        self.log("Person: " + entity + ": "+ old + " --> " + new)
        # Change house_mode to Away if everyone is away.
        if self.noone_home():
            self.log("No one is home")
            self.select_option("input_select.house_mode", self.const.HOUSE_MODE_AWAY)
        # Change house_mode to Home if anyone is home and the house_mode is set to Away.
        elif self.anyone_home() and self.get_state("input_select.house_mode") == self.const.HOUSE_MODE_AWAY:
            self.log("Someone is home")
            self.select_option("input_select.house_mode", self.const.HOUSE_MODE_HOME)

    def wake_up_callback(self, kwargs):
        # Change house_mode to Home only if it is currently set to Asleep
        if self.get_state("input_select.house_mode") == self.const.HOUSE_MODE_ASLEEP:
            self.select_option("input_select.house_mode", self.const.HOUSE_MODE_HOME)
