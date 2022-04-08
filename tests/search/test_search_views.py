from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import TestCase, Client, RequestFactory

from app.search import views
from app.usermanager import models


class TestSearchViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.url_search = reverse("search")

        self.user1 = {
            'email': 'testemail1@gmail.com',
            'username': 'username',
            'password': 'password1'
        }

        models.User.objects.create_user(**self.user1)
        self.user = models.User.objects.get(email=self.user1["email"])
        return super().setUp()

    def test_get_search_view_with_anonymous_user(self):
        request = self.factory.get(self.url_search)
        request.user = AnonymousUser()
        response = views.search(request)
        self.assertEqual(response.status_code, 302)

    def test_get_search_view_with_user(self):
        request = self.factory.get(self.url_search)
        request.user = self.user
        response = views.search(request)
        self.assertEqual(response.status_code, 200)
