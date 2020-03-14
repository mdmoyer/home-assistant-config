import appdaemon.plugins.hass.hassapi as hass
import datetime

class LightsSchedule(hass.Hass):

  def initialize(self):
    self.const = self.get_app("const")
    # Turn living room lights on weekday mornings, only if the sun is still down.
    self.run_daily(self.lights_on_morning, datetime.time(6, 0, 0), constrain_days = "mon,tue,wed,thu,fri", constrain_end_time = "sunrise")
    # Turn off living room lights on weekday mornings when the sun rises.
    self.run_at_sunrise(self.lights_off_morning, constrain_days = "mon,tue,wed,thu,fri")
    # Turn off living room lights on weekday mornings when Mike leaves for work.
    self.listen_state(self.lights_off_away, entity="person.mm", old=self.const.PERSON_HOME, new=self.const.PERSON_AWAY, constrain_days = "mon,tue,wed,thu,fri", constrain_end_time = "sunrise")
    # Turn on living room lights 60 minutes before sunset.
    self.run_at_sunset(self.lights_on_evening, offset = -60 * 60)

  def lights_on_morning(self, kwargs):
    # Turn on the living room light, brightness at 1/3.
    self.turn_on("light.living_room", brightness=85)

  def lights_off_morning(self, kwargs):
    # Turn off the living room light, reset brightness to full for later.
    self.turn_on("light.living_room", brightness=255)
    self.turn_off("light.living_room")

  def lights_off_away(self, entity, attribute, old, new, kwargs):
    # Turn off the living room light, reset brightness to full for later.
    self.turn_off("light.living_room")

  def lights_on_evening(self, kwargs):
    self.turn_on("light.living_room", brightness=255)
