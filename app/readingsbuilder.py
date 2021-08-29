from datetime import datetime

import time


class readingsbuilder:
    readings_structrue = {}

    def __init__(self, thp_readings, light_intensity_readings, camera_mode):
        self.light_intensity_readings = light_intensity_readings
        self.thp_readings = thp_readings
        self.camera_mode = camera_mode

    def build_tcp_readings(self):
        for thp in self.thp_readings["s_readings"]:
            if thp["s_type"] == "TEMP":
                self.readings_structrue["temperature"] = float(thp["s_data"])
            if thp["s_type"] == "HUMID":
                self.readings_structrue["humidity"] = float(thp["s_data"])
            if thp["s_type"] == "PRESS":
                pressure = float(thp["s_data"])
                self.readings_structrue["pressure"] = pressure / 100.0
                self.readings_structrue["pressure_mmhg"] = round(
                    pressure / 133)

    def build_light_readings(self):
        self.readings_structrue["light"] = float(
            self.light_intensity_readings["s_data"])

    def build_cam_mode(self):
        cam_mode = self.camera_mode["mode"]
        if cam_mode == "NORM":
            self.readings_structrue["camera_mode"] = "Normal mode"
        elif cam_mode == "NIGHT":
            self.readings_structrue["camera_mode"] = "Night-vision mode"

    def build_readings_structrue(self):
        self.readings_structrue["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if "s_readings" in self.thp_readings and len(self.thp_readings["s_readings"]) > 0:
            self.build_tcp_readings()
        if "s_type" in self.light_intensity_readings:
            self.build_light_readings()
        if "mode" in self.camera_mode:
            self.build_cam_mode()
        return self.readings_structrue
