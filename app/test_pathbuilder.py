import unittest
from os import path
from datetime import datetime
import json
from pathbuilder import pathbuilder


class test_pathbuilder(unittest.TestCase):

    def setUp(self):
        self.timestamp = "2021-05-20 01:25:55"

    def test_build_file_name(self):
        pb = pathbuilder("/tmp", ".jpeg", self.timestamp)
        self.assertEqual(pb.build_file_name(), "012555.jpeg")

    def test_build_dir_path(self):
        pb = pathbuilder("/tmp", ".jpeg", self.timestamp)
        self.assertEqual(pb.build_dir_path(), "/tmp/20210520")

    def test_create_dir(self):
        pb = pathbuilder("/tmp", ".jpeg", self.timestamp)
        dir_path = pb.create_dir()
        self.assertTrue(path.exists(dir_path))
        self.assertEqual(dir_path, "/tmp/20210520")

    def test_build_file_path(self):
        pb = pathbuilder("/tmp", ".jpeg", self.timestamp)
        dir_path = pb.create_dir()
        self.assertEqual(pb.build_file_path(), "/tmp/20210520/012555.jpeg")

    if __name__ == '__main__':
        unittest.main()
