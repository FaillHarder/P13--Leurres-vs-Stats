from django.contrib.auth import get_user_model
from django.test import TestCase

from app.adddata import models
from app.fishingstats.create_stats import FishingStats


class TestFishingStats(TestCase):

    def setUp(self):
        self.identifier = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'password'
        }
        self.user = get_user_model().objects.create(**self.identifier)

        # create CatchFish.object n°1 with stickbait/ayu/Ensoleillé/Clair
        self.lure_stickbait = models.Lure.objects.create(name="stickbait")
        self.color_ayu = models.Color.objects.create(name="ayu")
        self.sky_state = "Ensoleillé"
        self.water_state = "Clair"
        self.catch_1 = models.CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure_stickbait,
            color_lure=self.color_ayu,
            sky_state=self.sky_state,
            water_state=self.water_state
        )
        # create CatchFish.object n°1 with popper/ayu/Ensoleillé/Clair
        self.lure_popper = models.Lure.objects.create(name="popper")
        self.catch_2 = models.CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure_popper,
            color_lure=self.color_ayu,
            sky_state=self.sky_state,
            water_state=self.water_state
        )
        return super().setUp()

    def test_top_lure_by_states(self):
        result = FishingStats().top_lure_by_states(self.sky_state, self.water_state)
        self.assertEqual(
            result,
            {f"{self.lure_stickbait}": 50.0, f"{self.lure_popper}": 50.0}
        )

    def test_top_color_by_states(self):
        result = FishingStats().top_color_by_states(self.sky_state, self.water_state)
        self.assertEqual(result, {f"{self.color_ayu}": 100.0})

    def test_top_overall_lure_and_color(self):
        result = FishingStats().top_overall_lure_and_color()
        self.assertEqual(
            result,
            (
                {f"{self.lure_stickbait}": 50.0, f"{self.lure_popper}": 50.0},
                {f"{self.color_ayu}": 100.0}
            )
        )
