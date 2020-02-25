import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class HouseMode(hass.Hass):

    def initialize(self):
        self.listen_state(self.log_house_mode_callback, 'input_select.house_mode')
        self.listen_state(self.away_mode_activated_callback, 'input_select.house_mode', new = "Away")
        self.listen_state(self.away_mode_deactivated_callback, 'input_select.house_mode', old = "Away")
        self.listen_state(self.sleep_mode_activated_callback, 'input_select.house_mode', new = "Asleep")
        self.listen_state(self.sleep_mode_deactivated_callback, 'input_select.house_mode', old = "Asleep")
        self.run_daily(self.deactivate_sleep_mode_callback, "07:00:00", old = "Asleep")

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

    def sleep_mode_deactivated_callback(self, entity, attribute, old, new, kwargs):
        self.log("I should now end temp regulation...but I don't.")
        temp_control = self.get_app('TempControl')
        temp_control.end_regulate_temp("climate.dining_room_nest")

    def deactivate_sleep_mode_callback(self, entity, attribute, old, new, kwargs):
        self.log("Dectivating sleep mode")
        self.select_option("input_select.house_mode", "Home")
