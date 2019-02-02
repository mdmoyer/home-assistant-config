import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class DoorActivatedLight(hass.Hass):

    def initialize(self):
        self.timer_handle = None
        self.listen_state(self.door_opened, entity=self.args["door_sensor"])

    def door_opened(self, entity, attribute, old, new, kwargs):
        if new == "on": 
            # Turn on light when door is opened.
            self.turn_on(self.args["light"])
            # Reset the timer, then set it to turn off the lights after a delay.
            self.cancel_timer(self.timer_handle)
            self.timer_handle = self.run_in(self.light_off, self.args["delay"])
        elif new == "off": 
            # Turn off light when door is opened.
            self.turn_off(self.args["light"])

    def light_off(self, kwargs):
        self.turn_off(self.args["light"])
