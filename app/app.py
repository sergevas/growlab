#!/bin/python3

import json
import os
import sys
import io
from PIL import Image
from specimen import specimen
from growlab_v1_http_client import growlab_v1_http_client
from readingsbuilder import readingsbuilder
from pathbuilder import pathbuilder

if __name__ == "__main__":
    print("Starting growlab")

    config = {}
    try:
        with open("./config.json") as f:
            config = json.loads(f.read())
    except Exception as e:
        sys.stderr.write("Error: {}".format(e))
        sys.exit(1)

    print("Loaded config, saving images every {} seconds to {}".format(
        config["images"]["interval_seconds"], config["images"]["output_directory"]))

    http_client = growlab_v1_http_client(config["http"])
    thp_readings = http_client.get_thp_readings()
    light_intensity_readings = http_client.get_light_intensity_readings()
    camera_mode = http_client.get_camera_mode()

    r_builder = readingsbuilder(
        thp_readings, light_intensity_readings, camera_mode)

    readings = r_builder.build_readings_structrue()

    print(readings)

    timestamp_string = readings["time"]

    readings_pathbuilder = pathbuilder(config["data"]["output_directory"],
                                       "." + config["data"]["encoding"], timestamp_string)

    readings_filepath = readings_pathbuilder.build_file_path()

    with open(readings_filepath, 'w') as readings_output_file:
        json.dump(readings, readings_output_file)

    frame = io.BytesIO(http_client.get_camera_image())

    pwd = os.getcwd()
    output_path = pwd + "/html"

    try:
        os.mkdir(output_path)
    except:
        pass

    spec = specimen(config["text"], config["images"])
    spec.save_image("{}/image.jpg".format(pwd), frame, readings)

    spec.save_html("{}/image.jpg".format(pwd), output_path, readings)
