import unittest
import json
from readingsbuilder import readingsbuilder


class test_readingsbuilder(unittest.TestCase):

    def setUp(self):
        thp_readings_1 = {
            "s_readings": [
                {
                    "s_id": "60",
                    "s_type": "TEMP",
                    "s_data": "26.079965189471842",
                    "s_timestamp": "2021-08-22T18:10:55.736630Z"
                },
                {
                    "s_id": "60",
                    "s_type": "HUMID",
                    "s_data": "45.481067387147625",
                    "s_timestamp": "2021-08-22T18:10:55.736630Z"
                },
                {
                    "s_id": "60",
                    "s_type": "PRESS",
                    "s_data": "99556.74677629767",
                    "s_timestamp": "2021-08-22T18:10:55.736630Z"
                }
            ]
        }

        light_intensity_readings_1 = {
            "s_type": "LIGHT",
            "s_data": "1.67",
            "s_timestamp": "2021-08-22T22:44:20.369467Z"
        }

        camera_mode_1 = {
            "mode": "NORM",
            "mode_timestamp": "2021-08-22T16:02:11.452302Z"
        }

        readings_timestamp = "2021-08-22 22:44:20"

        self.read_build_1 = readingsbuilder(
            thp_readings_1, light_intensity_readings_1, camera_mode_1, readings_timestamp)

        self.maxDiff = None

    def test_build_readings_structrue(self):
        expected_readings = {'time': '2021-08-22 22:44:20', 'temperature': 26.079965189471842, 'humidity': 45.481067387147625,
                             'pressure': 995.5674677629768, 'pressure_mmhg': 749, 'light': 1.67, 'camera_mode': 'Normal mode'}
        actual_readings = self.read_build_1.build_readings_structrue()
        self.assertEqual(actual_readings, expected_readings)

    if __name__ == '__main__':
        unittest.main()
