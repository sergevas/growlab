import os

from datetime import datetime


class pathbuilder:
    def __init__(self, base_path, ext, timestamp_string):
        self.base_path = base_path
        self.ext = ext
        self.timestamp = datetime.strptime(
            timestamp_string, "%Y-%m-%d %H:%M:%S")

    def build_dir_path(self):
        current_dir_name = self.timestamp.strftime("%Y%m%d")
        dir_path = self.base_path + "/" + current_dir_name
        return dir_path

    def build_file_name(self):
        return self.timestamp.strftime("%H%M%S") + self.ext

    def create_dir(self):
        dir = self.build_dir_path()
        if os.path.exists(dir) == False:
            os.makedirs(dir)
        return dir

    def build_file_path(self):
        file_path = self.create_dir() + "/" + self.build_file_name()
        return file_path
