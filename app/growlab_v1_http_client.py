import requests
from requests_toolbelt import sessions
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


DEFAULT_RESPONSE = {}


class growlab_v1_http_client:
    def __init__(self, config):
        self.config = config

        retry_strategey = Retry(
            total=self.config["retryAttemts"],
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST", "PUT"])
        adapter = HTTPAdapter(max_retries=retry_strategey)

        self.http = sessions.BaseUrlSession(base_url=self.config["base_url"])
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def get_thp_readings(self):
        try:
            response = self.do_request("/growlab/api/v1/sensors/thp").json()
        except AttributeError:
            response = DEFAULT_RESPONSE
        return response

    def get_light_intensity_readings(self):
        try:
            response = self.do_request("/growlab/api/v1/sensors/light").json()
        except AttributeError:
            response = DEFAULT_RESPONSE
        return response

    def get_camera_mode(self):
        try:
            response = self.do_request(
                "/growlab/api/v1/actuators/camera/mode").json()
        except AttributeError:
            response = DEFAULT_RESPONSE
        return response

    def get_camera_image(self):
        try:
            response = self.do_request(
                "/growlab/api/v1/actuators/camera/image").content
        except AttributeError:
            response = bytearray()
        return response

    def do_request(self, resource_url):
        response = ''
        try:
            response = self.http.get(
                resource_url, timeout=self.config["timeout"])
            response.raise_for_status()
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as err:
            pass
        return response
