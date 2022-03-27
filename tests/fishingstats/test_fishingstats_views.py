from app.fishingstats import views

from django.test import TestCase, Client


class FishingStatsView(TestCase):

    def setUp(self):
        self.client = Client()
        return super().setUp()

    def test_stats_view(self):
        request = self.client.get('/stats/')
        response = views.stats(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Statistiques")
