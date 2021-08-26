import requests


class growlab_v1_http_client:
    def __init__(self, config):
        self.config = config

    def get_thp_readings(self):
        return self.do_request("/sensors/thp").json()

    def get_light_intensity_readings(self):
        return self.do_request("/sensors/light").json()

    def get_camera_mode(self):
        return self.do_request("/actuators/camera/mode").json()

    def get_camera_image(self):
        return self.do_request("/actuators/camera/image").content

    def do_request(self, resource):
        response = ""
        try:
            resource_url = self.config["base_url"] + resource
            response = requests.get(
                resource_url, timeout=self.config["timeout"])
            response.raise_for_status()
        # Code here will only run if the request is successful
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        return response
