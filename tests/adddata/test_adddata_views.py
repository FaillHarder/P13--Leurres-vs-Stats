from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from app.adddata import models, forms


class TestAdddataViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_catchfish = reverse("catchfish")

        self.lure = models.Lure.objects.create(name="stickbait")
        self.color_lure = models.Color.objects.create(name="ayu")
        self.sky_state = models.SkyState.objects.create(name="ensoleillé")
        self.water_state = models.WaterState.objects.create(name="clair")

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

    def test_post_catchfish(self):
        self.client.login(
            email=self.identifier["email"],
            password=self.identifier["password"]
        )
        data = {
            "lure": self.lure.pk,
            "color_lure": self.color_lure.pk,
            "sky_state": self.sky_state.pk,
            "water_state": self.water_state.pk
        }
        response = self.client.post(self.url_catchfish, data)
        self.assertEqual(response.status_code, 302)

        form = forms.CatchFishForm(data=data)
        self.assertTrue(form.is_valid())

        catch_fish = form.save(commit=False)
        catch_fish.fisherman = self.user
        result = models.CatchFish.objects.count()
        self.assertEqual(result, 1)
        catch_fish_obj = models.CatchFish.objects.all()
        self.assertTrue(
            catch_fish_obj.__str__,
            "(stickbait/ayu) (Ciel Ensoleillé/Eau Trouble). Pécheur : testemail@gmail.com>"
        )

    def test_get_catchfish_view_with_anonymoususer(self):
        response = self.client.get(self.url_catchfish)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/add/catchfish")
