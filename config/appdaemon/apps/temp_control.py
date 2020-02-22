import appdaemon.plugins.hass.hassapi as hass
import datetime
import logging

class TempControl(hass.Hass):

    # Constants
    HVAC_MODE_HEAT = "heat"
    HVAC_MODE_COOL = "cool"
    HVAC_ACTION_IDLE = "idle"

    def initialize(self):
        # Regulate temperature everytime the sensor reports a temperature change.
        self.listen_state(self.regulate_temp_callback, self.args["sensor_temp"])
        # Regulate temperature everytime the HVAC turns itself on or off.
        self.listen_state(self.regulate_temp_callback, climate_entity, attribute = "hvac_action")
        # At the end of the period of temperature regulation, reset the temperature. Subtract 1 second to ensure it runs before the end constraint kicks in.
        end_time = (datetime.datetime.strptime(self.args["constrain_end_time"], '%H:%M:%S') - datetime.timedelta(seconds=1)).time()
        self.run_daily(self.end_temp_regulation_callback, end_time)

    def regulate_temp_callback(self, entity, attribute, old, new, kwargs):
        self.regulate_temp()

    def end_temp_regulation_callback(self, kwargs):
        hvac_mode = self.get_state(self.args["climate_entity"])
        reset_temp = 75 if hvac_mode == self.HVAC_MODE_COOL else 65 if hvac_mode == self.HVAC_MODE_HEAT else 70
        self.set_climate(hvac_mode, reset_temp)

    def regulate_temp(self):
        climate_entity = self.args["climate_entity"]
        sensor_temp = float(self.get_state(self.args["sensor_temp"]))
        min_temp = float(self.args["min_temp"])
        max_temp = float(self.args["max_temp"])
        climate_curr_temp = float(self.get_state(climate_entity, attribute = "current_temperature"))
        hvac_mode = self.get_state(climate_entity)
        # Indicates whether the HVAC is actively "heating" or "cooling". If neither, it is "idle".
        hvac_action = self.get_state(climate_entity, attribute = "hvac_action")

        # If the HVAC is not running, determine if things are too hot or too cold.
        if hvac_action == self.HVAC_ACTION_IDLE:
            # If temperature is too high, begin cooling.
            if sensor_temp > max_temp:
                self.set_climate(self.HVAC_MODE_COOL, climate_curr_temp - 2)
            # If temperature is too low, begin heating.
            elif sensor_temp < min_temp:
                self.set_climate(self.HVAC_MODE_HEAT, climate_curr_temp + 2)
        # If the HVAC is running but the temperature is comfortable, stop the HVAC.
        elif sensor_temp > min_temp + 1 and sensor_temp < max_temp - 1:
            self.set_climate(hvac_mode, climate_curr_temp + 1 if hvac_mode == self.HVAC_MODE_COOL else climate_curr_temp - 1 if hvac_mode == self.HVAC_MODE_HEAT else climate_curr_temp)

    def set_climate(self, hvac_mode, new_target):
        climate_entity = self.args["climate_entity"]
        sensor_temp = float(self.get_state(self.args["sensor_temp"]))
        climate_temp = self.get_state(climate_entity, attribute = "current_temperature")
        old_target = self.get_state(climate_entity, attribute = "temperature")
        hvac_action = self.get_state(climate_entity, attribute = "hvac_action")
        self.log("Sensor: " + str(sensor_temp) + ", Climate: " + str(climate_temp) + " (" + str(hvac_action) + "), Target: " + str(old_target) + " -> " + str(new_target) + " (" + str(hvac_mode) + ")")
        self.call_service('climate/set_hvac_mode', entity_id = climate_entity, hvac_mode = hvac_mode)
        self.call_service('climate/set_temperature', entity_id = climate_entity, temperature = new_target)
