import unittest
import json
from readingsbuilder import readingsbuilder


class test_readingsbuilder(unittest.TestCase):

    def test_get_thp_readings(self):
        growlab_v1_http_client = growlab_v1_http_client(config)
        expected_thp_readings = {
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
        actual_thp_readings = growlab_v1_http_client.get_thp_readings()
        self.assertEqual(actual_thp_readings, expected_thp_readings)

    def test_get_light_intensity_readings(self):
        expected_light_intensity_readings = {
            "s_type": "LIGHT",
            "s_data": "1.67",
            "s_timestamp": "2021-08-22T22:44:20.369467Z"
        }
        actual_light_intensity_readings = growlab_v1_http_client.get_light_intensity_readings()
        self.assertEqual(actual_light_intensity_readings,
                         expected_light_intensity_readings)

    def test_get_camera_mode(self):
        expected_camera_mode = {
            "mode": "NIGHT",
            "mode_timestamp": "2021-08-22T16:02:11.452302Z"
        }
        actual_camera_mode = growlab_v1_http_client.get_camera_mode()
        self.assertEqual(actual_camera_mode, expected_camera_mode)

    def test_get_camera_image(self):
        expected_camera_image = ""
        actual_camera_image = ""
        self.assertEqual(actual_camera_image, expected_camera_image)

    def test_do_request(self):
        resource = "/actuators/camera/mode"
        expected_camera_mode = {
            "mode": "NIGHT",
            "mode_timestamp": "2021-08-22T16:02:11.452302Z"
        }
        actual_camera_mode = growlab_v1_http_client.do_request(resource)
        self.assertEqual(actual_camera_mode, expected_camera_mode)

    if __name__ == '__main__':
        unittest.main()
