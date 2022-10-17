from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_gis import filters as gis_filters

from rest_framework import (
    generics,
    response,
    permissions,
    status
)

from django.db.models import (
    Sum, OuterRef, Subquery, F, Case, When, Value, Count)

from monitoring import (
    serializers,
    models,
    filters as monitoring_filters
)

from django.db.models import (
    Sum, OuterRef, Subquery, F, Q, Case, When, Value, Count, FloatField, functions)


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
    """
    Group by:
        grouping (str):
            * monitoring_by_year
            * monitoring_by_co_funai
            * monitoring_by_co_funai_and_year
            * se 'grouping' for igual a None ou sem referencia retorna o DEFAULT que é o monitoring_by_day
    Filters:
        co_cr (list): filtering Regional Coordenation using code.
        co_funai (list): filtering Indigenou Lands using Funai code
        stage (list): stage name. E.g.: CR, DG, FF, DR
        start_date (str): filtering start date
        end_date (str): filteringend ende date
    """

    filterset_class = monitoring_filters.MonitoringConsolidatedStatsFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get_serializer_class(self):

        data_grouping = self.request.GET.get('grouping', None)

        if data_grouping == "monitoring_by_co_funai_and_year":
            return serializers.MonitoringConsolidatedStatsByCoFunaiAndYearSerializer
        elif data_grouping == "monitoring_by_co_funai":
            return serializers.MonitoringConsolidatedStatsByCoFunaiSerializer
        elif data_grouping == "monitoring_by_year":
            return serializers.MonitoringConsolidatedStatsByYearSerializer
        return serializers.ConsultaMonitoramentoTerraIndigenaSerializer

    def get_queryset(self):

        data_grouping = self.request.GET.get('grouping', None)

        if data_grouping == "monitoring_by_co_funai_and_year":
            return models.MonitoringConsolidatedStats.objects.values('co_funai', 'no_ti', 'ti_nu_area_ha', ano=functions.ExtractYear('dt_t_um')).annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("ano")
        elif data_grouping == "monitoring_by_year":
            return models.MonitoringConsolidatedStats.objects.values(ano=functions.ExtractYear('dt_t_um')).annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("ano")
        elif data_grouping == "monitoring_by_co_funai":
            return models.MonitoringConsolidatedStats.objects.values('co_funai', 'no_ti', 'ti_nu_area_ha').annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("no_ti")
        else:
            return models.MonitoringConsolidatedStats.objects.values('co_funai', 'no_ti', 'dt_t_um', 'ti_nu_area_ha',).annotate(total_nu_area_ha=Sum("nu_area_ha"), quantity_polygons=Count("no_estagio", output_field=FloatField()), cr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="CR")), dg_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DG")), dr_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="DR")), ff_nu_area_ha=Sum("nu_area_ha", filter=Q(no_estagio__exact="FF"))).order_by("dt_t_um")
