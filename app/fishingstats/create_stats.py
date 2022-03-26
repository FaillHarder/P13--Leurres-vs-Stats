from django.db.models import Count, Q

from app.adddata.models import CatchFish, Lure, Color


class FishingStats():

    def top_lure_by_states(self, sky_state, water_state):
        """Method to return lures stats compared with sky and water

        Args:
            sky_state (str): models.CatchFisht.sky_state choice
            water_state (str): models.CatchFisht.water_state choice

        Returns:
            dict:
                - key = name (lure)
                - value = percentage
        """
        query = Lure.objects.annotate(
            num=Count(
                "catchfish",
                filter=Q(catchfish__sky_state=sky_state) & Q(catchfish__water_state=water_state)
                )
            ).order_by("-num")
        return FishingStats.convert_to_percentage(query)

    def top_color_by_states(self, sky_state, water_state):
        query = Color.objects.annotate(
            num=Count(
                "catchfish",
                filter=Q(catchfish__sky_state=sky_state) & Q(catchfish__water_state=water_state)
                )
            ).order_by("-num")
        return FishingStats.convert_to_percentage(query)

    def top_overall_lure_and_color(self):
        """method to return overall lures and colors stats

        Returns:
            tuple :
                    {lure_name: percentage},
                    {color_name: percentage}
        """
        top_lure = FishingStats.convert_to_percentage(
            Lure.objects.annotate(num=Count("catchfish")).order_by("-num")
        )
        top_color = FishingStats.convert_to_percentage(
            Color.objects.annotate(num=Count("catchfish")).order_by("-num")
        )
        return top_lure, top_color

    @staticmethod
    def convert_to_percentage(query_set):
        """Method to convert queryset integer value to percentage

        Args:
            query_set (queryset): return from :
                - top_lure_by_states
                - top_color_by_states
                - top_overall_lure_and_color

        Returns:
            dict:
                - key = name (lure or color)
                - value = percentage
        """
        catchfish = CatchFish.objects.all()
        catchfish_len = len(catchfish)
        query_set_len = len(query_set)
        dict_percent = {}
        for i in range(0, query_set_len):
            dict_percent[f"{query_set[i]}"] = round(query_set[i].num*100/catchfish_len, 2)
        return dict_percent
