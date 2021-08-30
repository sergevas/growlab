#!/bin/python3

import json
import os
import sys
import io
import time

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

    print("Loaded config, saving images to {}".format(
        config["images"]["output_directory"]))

    http_client = growlab_v1_http_client(config["http"])
    thp_readings = http_client.get_thp_readings()
    light_intensity_readings = http_client.get_light_intensity_readings()
    camera_mode = http_client.get_camera_mode()
    timestamp_string = time.strftime("%Y-%m-%d %H:%M:%S")

    r_builder = readingsbuilder(
        thp_readings, light_intensity_readings, camera_mode, timestamp_string)

    readings = r_builder.build_readings_structrue()

    # print(readings)

    readings_pathbuilder = pathbuilder(config["data"]["output_directory"],
                                       "." + config["data"]["encoding"], timestamp_string)

    readings_filepath = readings_pathbuilder.build_file_path()

    print("Readings file output path [", readings_filepath, "]")

    with open(readings_filepath, 'w') as readings_output_file:
        json.dump(readings, readings_output_file)

    is_image_taken = False
    camera_image = http_client.get_camera_image()
    if len(camera_image) != 0:
        is_image_taken = True

    if is_image_taken:
        frame = io.BytesIO(http_client.get_camera_image())

    pwd = os.getcwd()
    output_path = pwd + "/html"
    # print("Html page content output path [", output_path, "]")
    try:
        os.mkdir(output_path)
    except:
        pass

    spec = specimen(config["text"], config["images"])
    pb = pathbuilder(config["images"]["output_directory"],
                     "." + config["images"]["encoding"], timestamp_string)
    image_file_path = pb.build_file_path()
    if is_image_taken:
        spec.save_image(image_file_path, frame, readings)
    spec.save_html(image_file_path, output_path, readings, is_image_taken)
