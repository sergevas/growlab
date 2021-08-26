from datetime import datetime

import time


class readingsbuilder:
    def __init__(self, thp_readings, light_intensity_readings, camera_mode):
        self.light_intensity_readings = light_intensity_readings
        self.thp_readings = thp_readings
        self.camera_mode = camera_mode

    def build_readings_structrue(self):
        readings_structrue = {}
        readings_structrue["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        print(self.thp_readings["s_readings"])
        for thp in self.thp_readings["s_readings"]:
            if thp["s_type"] == "TEMP":
                readings_structrue["temperature"] = float(thp["s_data"])
            if thp["s_type"] == "HUMID":
                readings_structrue["humidity"] = float(thp["s_data"])
            if thp["s_type"] == "PRESS":
                pressure = float(thp["s_data"])
                readings_structrue["pressure"] = pressure / 100.0
                readings_structrue["pressure_mmhg"] = round(pressure / 133)
        readings_structrue["light"] = float(
            self.light_intensity_readings["s_data"])
        cam_mode = self.camera_mode["mode"]
        if cam_mode == "NORM":
            readings_structrue["camera_mode"] = "Normal mode"
        elif cam_mode == "NIGHT":
            readings_structrue["camera_mode"] = "Night-vision mode"
        return readings_structrue
