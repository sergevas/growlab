#!/bin/python3

import json
import os
import sys
from sensors import growbme280
from camera import camera
from specimen import specimen
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

    bme280 = growbme280()

    readings = bme280.get_readings()
    readings_pathbuilder = pathbuilder(config["data"]["output_directory"],
                                       "." + config["data"]["encoding"], readings["time"])
    readings_filepath = readings_pathbuilder.build_file_path()
    with open(readings_filepath, 'w') as readings_output_file:
        json.dump(readings, readings_output_file)

    cam = camera(config["images"])
    frame = cam.get_frame()

    pwd = os.getcwd()
    output_path = pwd + "/html"

    try:
        os.mkdir(output_path)
    except:
        pass

    spec = specimen(config["text"], config["images"])

    pb = pathbuilder(config["images"]["output_directory"],
                     "." + config["images"]["encoding"], readings["time"])
    image_file_path = pb.build_file_path()

    spec.save_image(image_file_path, frame, readings)

    spec.save_html(image_file_path, output_path, readings)