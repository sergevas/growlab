import json
import os
import time
from datetime import datetime
from influxdb import InfluxDBClient


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    # Parse NodeMCU data packet into JSON
    r = json.loads(req)
    print("Have got a request: ", r)

    influx_host = os.getenv("influx_host")
    influx_port = os.getenv("influx_port")
    influx_db = os.getenv("influx_db")

    influx_user = get_file("/var/openfaas/secrets/influx-user")
    influx_pass = get_file("/var/openfaas/secrets/influx-pass")

    client = InfluxDBClient(influx_host, influx_port,
                            influx_user, influx_pass, influx_db)
    try:
        client.create_database(influx_db)
    except Exception as e:
        print("Unable to create Database ", influx_db)
        print(e)

    points = make_points(r)

    res = client.write_points(points)
    client.close()

    res_json = json.dumps(res)
    print("Have got a response", res_json)

    return res_json


def get_file(path):
    v = ""
    with open(path) as f:
        v = f.read()
        f.close()
    return v.strip()


def make_points(r):
    tags = {"sensor": r["sensor"]}
    my_date = datetime.now()
    iso_time = my_date.isoformat()
    points = []

    if "status" in r:
        points.append({
            "measurement": "status",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": r["status"]
            }
        })

    if "temperature" in r:
        points.append({
            "measurement": "temp",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": float(r["temperature"])
            }
        })

    if "cpu_temperature" in r:
        points.append({
            "measurement": "cpu_temperature",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": float(r["cpu_temperature"])
            }
        })

    if "disk_space_total" in r:
        points.append({
            "measurement": "disk_space_total",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": int(r["disk_space_total"])
            }
        })

    if "disk_space_free" in r:
        points.append({
            "measurement": "disk_space_free",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": int(r["disk_space_free"])
            }
        })

    if "heap_memory_total" in r:
        points.append({
            "measurement": "heap_memory_total",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": int(r["heap_memory_total"])
            }
        })

    if "heap_memory_free" in r:
        points.append({
            "measurement": "heap_memory_free",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": int(r["heap_memory_free"])
            }
        })

    if "heap_memory_max" in r:
        points.append({
            "measurement": "heap_memory_max",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": int(r["heap_memory_max"])
            }
        })

    if "heap_memory_used" in r:
        points.append({
            "measurement": "heap_memory_used",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": int(r["heap_memory_used"])
            }
        })

    if "humidity" in r:
        points.append({
            "measurement": "humidity",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": float(r["humidity"])
            }
        })

    if "pressure" in r:
        pressureInHg = float(r["pressure"]) / 3386
        points.append({
            "measurement": "pressure",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": pressureInHg
            }
        })

    if "light" in r:
        points.append({
            "measurement": "light",
            "tags":  tags,
            "time": iso_time,
            "fields": {
                "value": float(r["light"])
            }
        })

    return points
