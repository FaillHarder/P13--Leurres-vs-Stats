from app.usermanager import views

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, RequestFactory, Client


class TestUsermanagerViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.email = "test@test.fr"
        self.password = "-Openclassrooms85"
        return super().setUp()

    def test_get_create_user_view(self):
        request = self.factory.get("registrer")
        response = views.create_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créer un compte")

    def test_post_create_user_view(self):
        data = {
            "email": self.email,
            "password1": self.password,
            "password2": self.password
        }
        # create user
        response_post = self.client.post(reverse("registrer"), data)
        # redirect index
        self.assertEqual(response_post.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
