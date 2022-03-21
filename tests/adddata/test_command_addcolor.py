from app.adddata.models import Color
from app.adddata.management.commands.addcolor import Command

from django.core.management import call_command
from django.test import TestCase
from PIL import Image
import tempfile


class TestCommand(TestCase):

    def setUp(self):
        self.command = Command()
        self.temp_folder = tempfile.TemporaryDirectory()

        self.file_list = ["image1.jpg", "image2.jpeg", "image3.png"]
        self.name_and_extension = {
            "image1": ".jpg",
            "image2": ".jpeg",
            "image3": ".png"
        }
        return super().setUp()

    def test_color_list_from_folder_return_file_list(self):
        # create image1.jpg, image2.jpeg, image3.png into temp_folder
        self.create_image()
        result = self.command.create_color_list_from_folder(self.temp_folder.name)
        self.assertTrue(result == self.file_list)

    def test_split_name_and_extension(self):
        result = self.command.split_name_and_extension(self.file_list)
        self.assertTrue(result == self.name_and_extension)

    def test_create_color_lure_name_into_db(self):
        self.command.create_color_lure_name_into_db(self.name_and_extension)
        result = Color.objects.count()
        self.assertEqual(result, 3)

    def create_image(self):
        """Utils method for create 3 images into tempory directory
        """
        image1 = Image.new('RGB', (100, 100))
        image1.save(f"{self.temp_folder.name}/image1.jpg")
        image2 = Image.new('RGB', (100, 100))
        image2.save(f"{self.temp_folder.name}/image2.jpeg")
        image3 = Image.new('RGB', (100, 100))
        image3.save(f"{self.temp_folder.name}/image3.png")

    def test_mycommand_addcolor(self):
        args = []
        opts = {}
        call_command('addcolor', *args, **opts)
