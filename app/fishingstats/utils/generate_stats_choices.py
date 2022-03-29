from ..create_stats import FishingStats
from app.adddata.models import SkyState, WaterState


class AllStatsByChoices():

    sky_states = SkyState.objects.all()
    water_states = WaterState.objects.all()

    def choices_list(self):
        choices_list = []
        for sky_state in self.sky_states:
            for water_state in self.water_states:
                choices_list.append([sky_state.name, water_state.name])
        return choices_list

    def generate_all(self):
        choices_list = self.choices_list()
        all_stats_list = []
        for list in choices_list:
            all_stats_list.append(
                [
                    list[0], list[1],
                    FishingStats().top_lures_and_colors_by_states(list[0], list[1])
                ]
            )
        return all_stats_list
