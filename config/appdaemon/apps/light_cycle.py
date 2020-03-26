import appdaemon.plugins.hass.hassapi as hass
import datetime

class LightCycle(hass.Hass):

    def initialize(self):
        self.timers = dict()
        self.listen_state(self.cycle_callback, "input_boolean.light_cycle", new="on")
        self.listen_state(self.cycle_off_callback, "input_boolean.light_cycle", new="off")

    def cycle_callback(self, entity, attribute, old, new, kwargs):
        self.log("Light Cycle On")
        self.run_in(self.cycle_lights_recursive, 0, light="light.hue_color_lamp_1", color_id=1)
        self.run_in(self.cycle_lights_recursive, 0, light="light.hue_color_lamp_2", color_id=3)
        self.run_in(self.cycle_lights_recursive, 0, light="light.living_room_3", color_id=5)

    def cycle_off_callback(self, entity, attribute, old, new, kwargs):
        self.log("Light Cycle Off")
        self.cancel_timers()
        self.turn_on("light.hue_color_lamp_1", brightness=255, transition=0, kelvin=2700)
        self.turn_on("light.hue_color_lamp_2", brightness=255, transition=0, kelvin=2700)
        self.turn_on("light.living_room_3", brightness=255, transition=0, kelvin=2700)

    def cycle_lights_recursive(self, kwargs):
        light = kwargs.get('light')
        color_id = kwargs.get('color_id')
        self.turn_on(light, brightness=255, transition=1, rgb_color=self.get_rgb(color_id))
        color_id = color_id + 1 if color_id < 5 else 0
        if self.get_state("input_boolean.light_cycle") == "on":
            self.timers[light] = self.run_in(self.cycle_lights_recursive, 1, light=light, color_id=color_id)

    def cancel_timers(self):
        for key, timer in self.timers.items():
            self.cancel_timer(timer)

    def get_rgb(self, color_id):
        if (color_id == 0):
            # 0 = Magenta
            return [255, 0, 255]
        elif (color_id == 1):
            # 1 = Red
            return [255, 0, 0]
        elif (color_id == 2):
            # 2 = Yellow
            return [255, 255, 0]
        elif (color_id == 3):
            # 3 = Green
            return [0, 255, 0]
        elif (color_id == 4):
            # 4 = Cyan
            return [0, 255, 255]
        elif (color_id == 5):
            # 5 = Blue
            return [0, 0, 255]
        else:
            # For unknown value, return white.
            return [255, 255, 255]
