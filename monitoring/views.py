from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters

from rest_framework import (
    generics,
    response,
    permissions,
    status
)
from django.db.models import (
    Sum,
    Q,
    Count,
    FloatField,
    functions
)

from monitoring import (
    serializers,
    models,
    filters as monitoring_filters
)


class AuthModelMixIn:
    """Default Authentication for `monitoring` views."""

    permission_classes = (permissions.AllowAny,)


class MonitoringConsolidatedView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data for `monitoring.models.MonitoringConsolidated`.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * stage (list): stage name. E.g.: CR, DG, FF, DR.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedSerializer
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        gis_filters.InBBoxFilter,
        DjangoFilterBackend,
    )


class MonitoringConsolidatedDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Detail data for `monitoring.MonitoringConsolidated`.

    Filters:
        * id (int): filtering request poligon identifier.
    """

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedDetailSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)


class MonitoringConsolidatedMapStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrieves `monitoring.MonitoringConsolidated` stats data.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * stage (list): stage name. E.g.: CR, DG, FF, DR.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedSerializer
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get(self, request) -> response.Response:
        """Get method to return stats for Monitoring.

        Returns sums for area_ha, area_km and registry.

        Args:
            request (Requests.request): Request data.

        Returns:
            response.Response: 
                django rest_framework.Response.response api response data.
        """
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            area_km=Sum('nu_area_km2'),
            total=Count('id')
        )
        return response.Response(data, status=status.HTTP_200_OK)


class MonitoringConsolidatedClassesView(AuthModelMixIn, generics.ListAPIView):
    """Lists abbreviation of types `stages` for `monitoring.MonitoringConsolidated`."""

    queryset = models.MonitoringConsolidated.objects.order_by(
        'no_estagio').distinct('no_estagio'
                               )
    serializer_class = serializers.MonitoringConsolidatedClassesSerializer


class MonitoringConsolidatedTableView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data for `monitoring.models.MonitoringConsolidated`.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * stage (list): stage name. E.g.: CR, DG, FF, DR.
        * start_date (str): filtering start date.
        * end_date (str): filtering end date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """

    queryset = models.MonitoringConsolidated.objects.all()
    serializer_class = serializers.MonitoringConsolidatedTableSerializer
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class MonitoringConsolidatedTableStatsView(AuthModelMixIn, generics.ListAPIView):
    """Return four data set acoording to the selected grouping in the request.

    Filters:
        co_cr (list): filtering Regional Coordenation using code.
        co_funai (list): filtering Indigenou Lands using Funai code.
        stage (list): stage name. E.g.: CR, DG, FF, DR.
        start_date (str): filtering start date.
        end_date (str): filteringend ende date.

    Group by:
        grouping (str): define applied data grouping. . E.g.:
            monitoring_by_co_funai,
            monitoring_by_year,
            monitoring_by_co_funai_and_year,
            monitoring_by_day or None or Any other

    Returns group by in request field grouping:
        * monitoring_by_year:
            `models.MonitoringConsolidatedStats` group by YEAR.
            `serializers.MonitoringConsolidatedStatsByYearSerializer`.
        * monitoring_by_co_funai:
            `models.MonitoringConsolidatedStats` group by CO_FUANI.
            `serializers.MonitoringConsolidatedStatsByCoFunaiSerializer`.
        * monitoring_by_co_funai_and_year:
            `models.MonitoringConsolidatedStats` group by CO_FUANI and YEAR.
            `serializers.MonitoringConsolidatedStatsByCoFunaiAndYearSerializer`.
        * DEFAULT is iquals monitoring_by_day:
            Used when request is None or not metch with keys previously listed.
            `models.MonitoringConsolidatedStats` group by CO_FUANI and YEAR.
            `serializers.MonitoringConsolidatedStatsByDaySerializer`.
    """

    filterset_class = monitoring_filters.MonitoringConsolidatedStatsFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get_serializer_class(self):
        """Get method to return one data set acoording to selected GROUPING.

        Returns one serializers class to `views.MonitoringConsolidatedTableStatsView`

        Returns:
            `serializers.MonitoringConsolidatedStatsByCoFunaiAndYearSerializer` or
            `serializers.MonitoringConsolidatedStatsByCoFunaiSerializer` or
            `serializers.MonitoringConsolidatedStatsByYearSerializer` or
            `serializers.MonitoringConsolidatedStatsByDaySerializer`.
        """
        data_grouping = self.request.GET.get('grouping', None)

        if data_grouping == "monitoring_by_co_funai_and_year":
            return serializers.MonitoringConsolidatedStatsByCoFunaiAndYearSerializer
        elif data_grouping == "monitoring_by_co_funai":
            return serializers.MonitoringConsolidatedStatsByCoFunaiSerializer
        elif data_grouping == "monitoring_by_year":
            return serializers.MonitoringConsolidatedStatsByYearSerializer
        return serializers.MonitoringConsolidatedStatsByDaySerializer

    def get_queryset(self):
        """Get method to return grouping data set acoording to selected GROUPING.

        Returns query grouping in class `views.MonitoringConsolidatedTableStatsView`.

        Returns:
            * Grouping `monitoring_by_co_funai_and_year`:
                `models.MonitoringConsolidatedStats` group by CO_FUANI and YEAR.
            * Grouping `monitoring_by_year`:
                `models.MonitoringConsolidatedStats` group by YEAR.
            * Grouping `monitoring_by_co_funai`:
                `models.MonitoringConsolidatedStats` group by CO_FUANI.
            * Grouping DEFAULT:
                `models.MonitoringConsolidatedStats` group by CO_FUANI and YEAR.
        """
        data_grouping = self.request.GET.get('grouping', None)

        if data_grouping == "monitoring_by_co_funai_and_year":
            return models.MonitoringConsolidatedStats.objects.values(
                'co_funai', 'no_ti', 'ti_nu_area_ha', ano=functions.ExtractYear('dt_t_um')).annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("ano")
        elif data_grouping == "monitoring_by_year":
            return models.MonitoringConsolidatedStats.objects.values(
                ano=functions.ExtractYear('dt_t_um')).annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("ano")
        elif data_grouping == "monitoring_by_co_funai":
            return models.MonitoringConsolidatedStats.objects.values(
                'co_funai', 'no_ti', 'ti_nu_area_ha').annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("no_ti")
        return models.MonitoringConsolidatedStats.objects.values('co_funai', 'no_ti', 'dt_t_um', 'ti_nu_area_ha',).annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("dt_t_um")
