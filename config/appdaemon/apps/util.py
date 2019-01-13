import appdaemon.plugins.hass.hassapi as hass
import datetime

class Util(hass.Hass):

    def initialize(self):
        pass
    
    def flash(self, kwargs):
        self.flashcount = 0
        self.run_in(self.flash_recursive, 1)
    
    def flash_recursive(self, kwargs):
        self.toggle("light.living_room")
        self.flashcount += 1
        if self.flashcount < 10:
          self.run_in(self.flash_recursive, 1)
