from ..create_stats import FishingStats, ChoicesTop
from app.adddata.models import SkyState, WaterState


class AllStatsByChoices():

    def choices_list(self):
        """Method to create a list of all combined sky/water states

        Returns:
            - list: for all combined sky/water states
                choices_list.append([sky_state.name, water_state.name])
        """
        choices_list = []
        sky_states = SkyState.objects.all()
        water_states = WaterState.objects.all()
        for sky_state in sky_states:
            for water_state in water_states:
                choices_list.append([sky_state.name, water_state.name])
        return choices_list

    def generate_all(self):
        """Method to create all statistics for lures and colors
        for all sky/water combos to return to the choice_list method

        Returns:
            list: for all list in choice_list:
                - all_stats_list.append(
                    [
                        skystate.name,
                        waterstate.name,
                        queryset : top lures by states,
                        queryset : top colors by states
                    ]
                )
        """
        choices_list = self.choices_list()
        all_stats_list = []
        for list in choices_list:
            all_stats_list.append(
                [
                    list[0], list[1],
                    FishingStats().top_by_states(ChoicesTop.LURE, list[0], list[1]),
                    FishingStats().top_by_states(ChoicesTop.COLOR, list[0], list[1])
                ]
            )
        return all_stats_list
