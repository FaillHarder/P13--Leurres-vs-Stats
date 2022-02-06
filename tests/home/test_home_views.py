from app.home import views

from django.test import TestCase, RequestFactory

class TestHomeView(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        return super().setUp()
    
    def test_index_view(self):
        request = self.factory.get('/')
        response = views.index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World!")
