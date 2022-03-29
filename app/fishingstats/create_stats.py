from django.db.models import Count, Q

from app.adddata.models import CatchFish, Lure, Color


class FishingStats():

    def top_lures_and_colors_by_states(self, sky_state, water_state):
        """Method to return lures stats compared with sky and water

        Args:
            sky_state (str): models.SkyState obj.name
            water_state (str): models.WaterState obj.name

        Returns:
            queryset:
                - key = name (lure)
                - value = percentage
        """
        query_lures = Lure.objects.annotate(
            num=Count(
                "catchfish",
                filter=Q(catchfish__sky_state__name=sky_state)
                & Q(catchfish__water_state__name=water_state)
                )
            ).order_by("-num")

        query_colors = Color.objects.annotate(
            num=Count(
                "catchfish",
                filter=Q(catchfish__sky_state__name=sky_state)
                & Q(catchfish__water_state__name=water_state)
                )
            ).order_by("-num")

        top_lures = FishingStats.convert_to_percentage(query_lures, sky_state, water_state)
        top_colors = FishingStats.convert_to_percentage(query_colors, sky_state, water_state)
        return top_lures, top_colors

    def top_overall_lures_and_colors(self):
        """method to return overall lures and colors stats

        Returns:
            tuple :
                    {lure_name: percentage},
                    {color_name: percentage}
        """
        top_lures = FishingStats.convert_to_percentage(
            Lure.objects.annotate(num=Count("catchfish")).order_by("-num")
        )
        top_colors = FishingStats.convert_to_percentage(
            Color.objects.annotate(num=Count("catchfish")).order_by("-num")
        )
        return top_lures, top_colors

    @staticmethod
    def convert_to_percentage(query_set, sky_state=None, water_state=None):
        """Method to convert queryset num value to percentage

        Args:
            query_set (queryset): return from :
                - top_lure_by_states
                - top_color_by_states
                - top_overall_lure_and_color

        Returns:
            queryset:
                - query.num = num percentage
        """
        catchfish = CatchFish.objects.all()
        if sky_state and water_state:
            catchfish_len = len(
                    catchfish.filter(sky_state__name=sky_state, water_state__name=water_state)
                )
        else:
            catchfish_len = len(catchfish)
        if catchfish_len > 0:
            for obj in query_set:
                obj.num = round(obj.num * 100 / catchfish_len, 2)
            return query_set
        else:
            return query_set
