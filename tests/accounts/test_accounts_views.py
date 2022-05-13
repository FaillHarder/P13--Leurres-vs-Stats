from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase, Client, RequestFactory

from app.accounts.models import Profile
from app.adddata.models import CatchFish, Lure, Color, SkyState, WaterState


class TestAccountsViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.url_profile = reverse("profile")
        self.url_edit_profile = reverse("edit_profile")

        self.lure = Lure.objects.create(name="stickbait")
        self.color_lure = Color.objects.create(name="ayu")
        self.sky_state = SkyState.objects.create(name="ensoleillé")
        self.water_state = WaterState.objects.create(name="clair")

        self.image = SimpleUploadedFile(
            name='test.png',
            content=open("static/assets/images/profile/profile_photo_test.png", 'rb').read(),
            content_type='image/png'
        )

        self.identifier = {
            'email': 'testemail2@gmail.com',
            'username': 'username',
            'password': 'password'
        }
        self.user = get_user_model().objects.create_user(**self.identifier)
        self.catch = CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure,
            color_lure=self.color_lure,
            sky_state=self.sky_state,
            water_state=self.water_state
        )
        return super().setUp()

    def test_profile_view(self):
        self.client.login(
            email=self.identifier["email"],
            password=self.identifier["password"]
        )
        response = self.client.get(self.url_profile)
        self.assertEqual(response.status_code, 200)
        # test default avatar in view
        self.assertContains(response, 'img src="/media/giphy_python.gif"')
        # test pseudo
        self.assertContains(response, "Testemail2")
        # test catchfish count
        self.assertContains(response, "Nombre de prise : 1")

    def test_edit_profile_view(self):
        self.client.login(
            email=self.identifier["email"],
            password=self.identifier["password"]
        )
        self.client.get(self.url_profile)
        response = self.client.get(self.url_edit_profile)
        self.assertTrue(response.status_code, 200)
        data = {
            "pseudo": "newpseudo",
            "name": "nomtest",
            "first_name": "prenomtest",
            "avatar": self.image
        }
        # edit profile with data
        self.client.post(self.url_edit_profile, data)
        response = self.client.get(self.url_profile)
        # test view content new pseudo name and first_name with title()
        self.assertContains(response, "Newpseudo")
        self.assertContains(response, "Nomtest")
        self.assertContains(response, "Prenomtest")
        self.assertContains(response, 'img src="/media/avatar/test.png"')

        user_profile = Profile.objects.get(user=self.user)
        self.assertTrue(user_profile.pseudo, "newpseudo")
        self.assertTrue(user_profile.name, "nomtest")
        self.assertTrue(user_profile.first_name, "prenomtest")
        self.assertTrue(user_profile.avatar, "test.png")
