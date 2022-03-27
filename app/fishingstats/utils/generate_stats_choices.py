from ..create_stats import FishingStats
from app.adddata.models import CatchFish


class AllStatsByChoices():

    sky_states = CatchFish.SKY_CHOICES
    water_states = CatchFish.WATER_CHOICES

    def choices_list(self):
        choices_list = []
        for sky_state in self.sky_states:
            for water_state in self.water_states:
                choices_list.append([sky_state[1], water_state[1]])
        return choices_list

    def generate_all(self):
        choices_list = self.choices_list()
        all_stats_list = []
        for list in choices_list:
            all_stats_list.append(
                [
                    f"Classement par condition météo. Ciel: {list[0]}/ Eau: {list[1]}",
                    FishingStats().top_lures_and_colors_by_states(list[0], list[1])
                ]
            )
        return all_stats_list
