from app.adddata.models import Color

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):

    help = "command to add default colors.jpg/jpeg/png to database from folder"

    IMAGE_EXTENSION = [".jpg", ".jpeg", ".png"]
    IMAGE_PATH = "static/assets/images/color_lure/"

    def handle(self, *args, **options):
        file_list = self.create_color_list_from_folder(self.IMAGE_PATH)
        file_dict = self.split_name_and_extension(file_list)
        self.create_color_lure_into_db(file_dict)

    def create_color_list_from_folder(self, folder_path):
        """method to create color name list from images in color_lure folder.
        Args:
            folder_path (str): self.IMAGE_PATH
        Returns:
            list: lure color name
        """
        file_list = os.listdir(folder_path)
        return file_list

    def split_name_and_extension(self, file_list):
        """Split image name and extension to return dict
        Args:
            file_list (list): image list from folder
        Returns:
            dict: key=image_name, value=image_extension
        """
        extention_list = self.IMAGE_EXTENSION
        name_and_extension = {}
        for name in file_list:
            for extension in extention_list:
                if extension in name:
                    name_and_extension[f"{name[:-len(extension)]}"] = extension
        return name_and_extension

    def create_color_lure_into_db(self, name_and_extension):
        """Create an object in the color model from a dictionary.
        Args:
            (dict): return -> split_name_and_extension()
        """
        for key, value in name_and_extension.items():
            Color.objects.get_or_create(name=key)
            color_object = Color.objects.get(name=key)
            if not color_object.image:
                image = SimpleUploadedFile(
                    name=f"{key}{value}",
                    content=open(f"{self.IMAGE_PATH}{key}{value}", 'rb').read(),
                    content_type=f'image/{value[1:]}'
                )
                color_object.image = image
                color_object.save()
