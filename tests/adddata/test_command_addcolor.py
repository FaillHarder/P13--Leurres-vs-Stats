from app.adddata.management.commands.addcolor import Command
from django.test import TestCase

import os
import tempfile


class TestCommand(TestCase):

    def setUp(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        self.temp_jpg = tempfile.NamedTemporaryFile(suffix=".jpg", dir=self.temp_folder.name)
        self.temp_jpg2 = tempfile.NamedTemporaryFile(suffix=".jpg", dir=self.temp_folder.name)

        self.file_list = ["image1.jpg", "image2.jpeg", "image3.png"]
        self.named_and_extension = {
            "image1": ".jpg",
            "image2": ".jpeg",
            "image3": ".png"
        }
        return super().setUp()

    def test_color_list_from_folder_return_file_list(self):
        file_list = os.listdir(self.temp_folder.name)
        result = Command().create_color_list_from_folder(self.temp_folder.name)
        self.assertTrue(result == file_list)

    def test_split_name_and_extension(self):
        result = Command().split_name_and_extension(self.file_list)
        self.assertTrue(result == self.named_and_extension)

    def test_create_color_lure_into_db(self):
        pass
