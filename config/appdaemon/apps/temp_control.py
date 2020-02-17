import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class TempControl(hass.Hass):

    def initialize(self):
        # Regulate temperature everytime the sensor reports a temperature change.
        self.listen_state(self.regulate_temp_callback, self.args["sensor_temp"])
        # Regulate temperature everytime the HVAC turns itself on or off.
        self.listen_state(self.regulate_temp_callback, self.args["climate_entity"], attribute = "hvac_action")
        # At the end of the period of temperature regulation, reset the temperature. Subtract 1 second to ensure it runs before the end constraint kicks in.
        end_time = (datetime.datetime.strptime(self.args["constrain_end_time"], '%H:%M:%S') - datetime.timedelta(seconds=1)).time()
        self.run_daily(self.end_temp_regulation_callback, end_time)

    def regulate_temp_callback(self, entity, attribute, old, new, kwargs):
        self.regulate_temp()

    def end_temp_regulation_callback(self, kwargs):
        climate_mode = self.get_state(self.args["climate_entity"], attribute = "hvac_mode")
        reset_temp = 75 if climate_mode == "cool" else 65 if climate_mode == "heat" else 70
        self.set_climate(climate_mode, reset_temp)

    def regulate_temp(self):
        sensor_temp = float(self.get_state(self.args["sensor_temp"]))

        # Sometimes sensor sends back 0 in error. Don't act on this behavior.
        if sensor_temp == 0:
            return

        min_temp = float(self.args["min_temp"])
        max_temp = float(self.args["max_temp"])
        climate_curr_temp = float(self.get_state(self.args["climate_entity"], attribute = "current_temperature"))
        climate_mode = self.get_state(self.args["climate_entity"], attribute = "hvac_mode")
        # Indicates whether the HVAC is actively "heating" or "cooling". If neither, it is "off".
        hvac_action = self.get_state(self.args["climate_entity"], attribute = "hvac_action")

        # If the HVAC is not running, determine if things are too hot or too cold.
        if hvac_action == "off":
            # If temperature is too high, begin cooling.
            if sensor_temp > max_temp:
                self.set_climate("cool", climate_curr_temp - 2)
            # If temperature is too low, begin heating.
            elif sensor_temp < min_temp:
                self.set_climate("heat", climate_curr_temp + 2)
        # If the HVAC is running but the temperature is comfortable, stop the HVAC.
        elif sensor_temp > min_temp + 1 and sensor_temp < max_temp - 1:
            self.set_climate(climate_mode, climate_curr_temp + 1 if climate_mode == "cool" else climate_curr_temp - 1 if climate_mode == "heat" else climate_curr_temp)

    def set_climate(self, climate_mode, new_target):
        sensor_temp = self.get_state(self.args["sensor_temp"])
        climate_temp = self.get_state(self.args["climate_entity"], attribute = "current_temperature")
        old_target = self.get_state(self.args["climate_entity"], attribute = "temperature")
        hvac_action = self.get_state(self.args["climate_entity"], attribute = "hvac_action")
        self.log("Sensor: " + str(sensor_temp) + ", Climate: " + str(climate_temp) + " (" + str(hvac_action) + "), Target: " + str(old_target) + " -> " + str(new_target) + " (" + str(climate_mode) + ")")
        self.call_service('climate/set_hvac_mode', hvac_mode = climate_mode)
        self.call_service('climate/set_temperature', temperature = new_target)
