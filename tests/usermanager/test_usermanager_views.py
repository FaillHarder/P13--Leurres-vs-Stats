from app.usermanager import models


from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client


class TestUsermanagerViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.url_create_user = reverse("registrer")
        self.url_login_user = reverse("login")
        self.url_logout = reverse("logout")

        self.user1 = {
            'email': 'testemail1@gmail.com',
            'username': 'username',
            'password': 'password1'
        }
        self.user2 = {
            'email': 'testemail2@gmail.com',
            'username': 'username',
            'password': 'password2'
        }

        self.user3 = {
            'email': 'testemail3@gmail.com',
            'username': 'username',
            'password': '-Openclassrooms85'
        }

        models.User.objects.create_user(**self.user1)
        models.User.objects.create_user(**self.user2)
        self.user = models.User.objects.get(email=self.user1["email"])
        return super().setUp()

    def test_get_create_user_view(self):
        response = self.client.get(self.url_create_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créer un compte")
        self.assertTemplateUsed(response, "usermanager/registrer.html")

    def test_post_create_user_view(self):
        data = {
            "email": self.user3["email"],
            "password1": self.user3["password"],
            "password2": self.user3["password"]
        }
        response = self.client.post(self.url_create_user, data)
        self.assertEqual(response.status_code, 302)
        # if user is created
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 3)

    def test_get_login_user_view(self):
        response = self.client.get(self.url_login_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Se connecter")
        self.assertTemplateUsed(response, "usermanager/login.html")

    def test_post_login_user_view(self):
        response = self.client.post(self.url_login_user, self.user2)
        self.assertEqual(response.status_code, 302)

    def test_post_login_user_view_whith_bad_email(self):
        data = {
            "email": "bademail@test.fr",
            "password": "badpassword"
        }
        response = self.client.post(self.url_login_user, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email ou mot de passe invalide.")

    def test_logout(self):
        self.client.login(
            email=self.user1["email"],
            password=self.user1["password"]
        )
        response = self.client.get(self.url_logout)
        self.assertEqual(response.status_code, 302)
