from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from app.adddata.models import SkyState, WaterState


class TestSearchViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.url_search = reverse("search")

        self.user1 = {
            'email': 'testemail1@gmail.com',
            'username': 'username',
            'password': 'password1'
        }

        get_user_model().objects.create_user(**self.user1)
        self.user = get_user_model().objects.get(email=self.user1["email"])

        SkyState.objects.create(name="ensoleillé")
        self.sky_state = SkyState.objects.first()
        WaterState.objects.create(name="clair")
        self.water_state = WaterState.objects.first()
        return super().setUp()

    def test_get_search_view_with_anonymous_user(self):
        response = self.client.get(self.url_search)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/search")

    def test_get_search_view_with_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url_search)
        self.assertContains(response, '<select name="skystate" id="id_skystate">')
        self.assertContains(response, '<select name="waterstate" id="id_waterstate">')
        self.assertEqual(response.status_code, 200)

    def test_post_search_view(self):
        data = {
            "skystate": self.sky_state.pk,
            "waterstate": self.water_state.pk
        }
        self.client.force_login(user=self.user)
        response = self.client.post(self.url_search, data)
        self.assertEqual(response.status_code, 200)
