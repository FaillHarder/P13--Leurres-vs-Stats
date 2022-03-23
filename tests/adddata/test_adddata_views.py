from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from app.adddata import models


class TestAdddataViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_catchfish = reverse("catchfish")

        self.lure = models.Lure.objects.create(name="stickbait")
        self.color_lure = models.Color.objects.create(name="ayu")
        self.sky_state = "Ensoleillé"
        self.water_state = "Trouble"

        self.identifier = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'password'
        }
        self.user = get_user_model().objects.create_user(**self.identifier)
        return super().setUp()

    def test_get_catchfish_view_with_user(self):
        self.client.login(
            email=self.identifier["email"],
            password=self.identifier["password"]
        )
        response = self.client.get(self.url_catchfish)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Couleur du leurre")
        self.assertTemplateUsed(response, "adddata/catchfish.html")

    def test_get_catchfish_view_with_anonymoususer(self):
        response = self.client.get(self.url_catchfish)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/add/catchfish")
