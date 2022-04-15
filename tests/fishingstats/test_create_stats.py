from django.contrib.auth import get_user_model
from django.test import TestCase

from app.adddata import models
from app.fishingstats.create_stats import FishingStats, ChoicesTop
from app.fishingstats.utils.generate_stats_choices import AllStatsByChoices


class TestFishingStats(TestCase):

    def setUp(self):
        self.identifier = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'password'
        }
        self.user = get_user_model().objects.create(**self.identifier)

        self.lure_stickbait = models.Lure.objects.create(name="stickbait")
        self.lure_popper = models.Lure.objects.create(name="popper")
        self.color_blue = models.Color.objects.create(name="blue")
        self.color_ayu = models.Color.objects.create(name="ayu")

        self.sky_state = models.SkyState.objects.create(name="ensoleillé")
        self.water_state = models.WaterState.objects.create(name="clair")
        self.water_state_trouble = models.WaterState.objects.create(name="trouble")

        # create CatchFish.object with stickbait/ayu/ensoleillé/clair
        self.catch_1 = models.CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure_stickbait,
            color_lure=self.color_ayu,
            sky_state=self.sky_state,
            water_state=self.water_state
        )

        # create CatchFish.object with popper/blue/ensoleillé/clair
        self.catch_2 = models.CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure_popper,
            color_lure=self.color_blue,
            sky_state=self.sky_state,
            water_state=self.water_state
        )

        # create CatchFish.object with stickbait/blue/ensoleillé/trouble
        self.catch_2 = models.CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure_stickbait,
            color_lure=self.color_blue,
            sky_state=self.sky_state,
            water_state=self.water_state
        )

        # create CatchFish.object with stickbait/blue/ensoleillé/clair
        self.catch_2 = models.CatchFish.objects.create(
            fisherman=self.user,
            lure=self.lure_stickbait,
            color_lure=self.color_blue,
            sky_state=self.sky_state,
            water_state=self.water_state_trouble
        )
        return super().setUp()

    def test_top_by_states(self):
        # test with choices_top=ChoicesTop.LURE
        result = FishingStats().top_by_states(
            choices_top=ChoicesTop.LURE,
            skystate=self.sky_state.name,
            waterstate=self.water_state.name
        )
        self.assertEqual(
            (result[0].name, result[0].num),
            (self.lure_stickbait.name, 66.67)
        )
        self.assertEqual(
            (result[1].name, result[1].num),
            (self.lure_popper.name, 33.33)
        )
        # test with choices_top=ChoicesTop.COLOR
        result = FishingStats().top_by_states(
            choices_top=ChoicesTop.COLOR,
            skystate=self.sky_state.name,
            waterstate=self.water_state.name
        )
        self.assertEqual(
            (result[0].name, result[0].num),
            (self.color_blue.name, 66.67)
        )
        self.assertEqual(
            (result[1].name, result[1].num),
            (self.color_ayu.name, 33.33)
        )

    def test_top_overall(self):
        # test with choices_top=ChoicesTop.LURE
        result = FishingStats().top_overall(choices_top=ChoicesTop.LURE)
        self.assertEqual(
            (result[0].name, result[0].num),
            (self.lure_stickbait.name, 75.00)
        )
        self.assertEqual(
            (result[1].name, result[1].num),
            (self.lure_popper.name, 25.00)
        )

        # test with choices_top=ChoicesTop.COLOR
        result = FishingStats().top_overall(choices_top=ChoicesTop.COLOR)
        self.assertEqual(
            (result[0].name, result[0].num),
            (self.color_blue.name, 75.00)
        )
        self.assertEqual(
            (result[1].name, result[1].num),
            (self.color_ayu.name, 25.00)
        )

    def test_catchfish_str_return(self):
        self.assertEqual(
            self.catch_1.__str__(),
            "(Stickbait/Ayu) (Ciel Ensoleillé/Eau Clair). Pécheur : testemail@gmail.com"
        )


class TestAllStatsByChoices(TestFishingStats):

    def test_choices_list(self):
        result = AllStatsByChoices().choices_list()
        self.assertEqual(
            result,
            [
                [self.sky_state.name, self.water_state.name],
                [self.sky_state.name, self.water_state_trouble.name]
            ]
        )

    def test_generate_all(self):
        result = AllStatsByChoices().generate_all()
        self.assertEqual(
            (result[0][0], result[0][1]),
            (self.sky_state.name, self.water_state.name)
        )
        self.assertEqual(
            (result[0][2][0].name, result[0][2][0].num),
            (self.lure_stickbait.name, 66.67)
        )
        self.assertEqual(
            (result[1][0], result[1][1]),
            (self.sky_state.name, self.water_state_trouble.name)
        )
        self.assertEqual(
            (result[1][2][0].name, result[1][2][0].num),
            (self.lure_stickbait.name, 100.0)
        )
