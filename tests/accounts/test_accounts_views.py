from app.accounts import views
from app.adddata.models import CatchFish, Lure, Color, SkyState, WaterState

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase, Client, RequestFactory

from PIL import Image


class TestAccountsViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.url_profile = reverse("profile")
        self.url_edit_profile = reverse("edit_profile")
        self.url_my_catch = reverse("my_catch")
        self.url_my_catch_edit = "my_catch/edit/"
        self.url_my_catch_delete = "my_catch/delete/"

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
        self.assertContains(response, 'img src="/static/assets/images/profile/default_avatar.gif"')
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
        self.assertContains(response, f'img src="/media/{self.user.profile.avatar}')

        self.assertTrue(self.user.profile.pseudo, "newpseudo")
        self.assertTrue(self.user.profile.name, "nomtest")
        self.assertTrue(self.user.profile.first_name, "prenomtest")
        self.assertTrue(self.user.profile.avatar, f'{self.user.profile.avatar}')
        # check profile_photo size before upload
        image = Image.open("static/assets/images/profile/profile_photo_test.png")
        self.assertTrue(image.size, (1024, 1024))
        # check profile_photo size after upload
        image_resize = Image.open(f'media/{self.user.profile.avatar}')
        self.assertTrue(image_resize.size, (600, 600))

    def test_my_catch_view(self):
        request = self.factory.get(self.url_my_catch)
        request.user = AnonymousUser()
        response = views.my_catch(request)
        # redirect to login
        self.assertTrue(response.status_code, 302)

        request.user = self.user
        response = views.my_catch(request)
        self.assertTrue(response.status_code, 200)
        # view content the only Catch
        self.assertTrue(response.content, '"<th scope="row">Stickbait</th><th scope="row">Stickbait</th>"')

    def test_my_catch_edit_view(self):
        request = self.factory.get(self.url_my_catch_edit)
        request.user = AnonymousUser()
        response = views.my_catch_edit(request, self.catch.pk)
        # redirect to login
        self.assertTrue(response.status_code, 302)

        request.user = self.user
        response = views.my_catch_edit(request, self.catch.pk)
        self.assertTrue(response.status_code, 200)

        # instance self.catch is selected in the edit form
        self.assertTrue(response.content, '<option value="1" selected>Stickbait')
        self.assertTrue(response.content, '<option value="1" selected>Ayu')
        self.assertTrue(response.content, '<option value="1" selected>Ensoleill')
        self.assertTrue(response.content, '<option value="1" selected>Clair')

    def test_my_catch_delete_view(self):
        request = self.factory.get(self.url_my_catch_delete)
        request.user = AnonymousUser()
        response = views.my_catch_delete(request, self.catch.pk)
        # redirect login
        self.assertTrue(response.status_code, 302)

        request.user = self.user
        response = views.my_catch_delete(request, self.catch.pk)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.content, "Voulez vous vraiment supprimer votre prise ?")
