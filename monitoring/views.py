from django.db.models import Count, DecimalField, FloatField, F, Q, Sum, functions, Value
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, response, status, exceptions
from rest_framework_gis import filters as gis_filters

from monitoring import filters as monitoring_filters
from monitoring import models, serializers


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


class MonitoringConsolidatedDetailView(
        AuthModelMixIn,
        generics.RetrieveAPIView
):
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
    """
    Lists abbreviation of types `stages` for 
    `monitoring.MonitoringConsolidated`."""

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

from django.shortcuts import render
class MonitoringConsolidatedTableStatsView(
    AuthModelMixIn,
    generics.ListAPIView
):
    """Return four data set acoording to the selected grouping in the request.

    Filters:
        * co_cr (list): filtering Regional Coordenation using code.
        * co_funai (list): filtering Indigenou Lands using Funai code.
        * stage (list): stage name. E.g.: CR, DG, FF, DR.
        * start_date (str): filtering start date.
        * end_date (str): filteringend ende date.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).

    Group by:
        grouping (str): define applied data grouping. . E.g.:
            monitoring_by_co_funai,
            monitoring_by_year,
            monitoring_by_co_funai_and_year,
            monitoring_by_day or None or Any other

    Returns group by in request field grouping:
        * monitoring_by_year:
            `models.MonitoringConsolidated` group by YEAR.
            `serializers.MonitoringConsolidatedByYearSerializer`.
        * monitoring_by_co_funai:
            `models.MonitoringConsolidated` group by CO_FUANI.
            `serializers.MonitoringConsolidatedByCoFunaiSerializer`.
        * monitoring_by_co_funai_and_year:
            `models.MonitoringConsolidated` group by CO_FUANI and YEAR.
            `serializers.MonitoringConsolidatedByCoFunaiAndYearSerializer`.
        * DEFAULT is iquals monitoring_by_day:
            Used when request is None or not metch with keys previously listed.
            `models.MonitoringConsolidated` group by CO_FUANI and YEAR.
            `serializers.MonitoringConsolidatedByDaySerializer`.
    """
    # queryset = models.MonitoringConsolidated.objects.all()
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

   

    def get_serializer_class(self):
        """Get method to return one data set acoording to selected GROUPING.

        Returns one serializers class to
        `views.MonitoringConsolidatedTableStatsView`

        Returns:
            `serializers.MonitoringConsolidatedByCoFunaiAndYearSerializer` or
            `serializers.MonitoringConsolidatedByCoFunaiSerializer` or
            `serializers.MonitoringConsolidatedByYearSerializer`or
            `serializers.MonitoringConsolidatedByDaySerializer`.
        """
        data_grouping = self.request.GET.get('grouping', None)

        if data_grouping == "monitoring_by_co_funai_and_year":
            return serializers.MonitoringConsolidatedByCoFunaiAndYearSerializer
        elif data_grouping == "monitoring_by_co_funai":
            return serializers.MonitoringConsolidatedByCoFunaiSerializer
        elif data_grouping == "monitoring_by_year":
            return serializers.MonitoringConsolidatedByYearSerializer
        return serializers.MonitoringConsolidatedByDaySerializer

    def get_queryset(self):
        """
        Get method to return grouping data set acoording to selected GROUPING.

        Returns query grouping in class
        `views.MonitoringConsolidatedTableStatsView`.

        Returns:
            * Grouping `monitoring_by_co_funai_and_year`:
                `models.MonitoringConsolidated`
                group by CO_FUANI and YEAR.

            * Grouping `monitoring_by_year`:
                `models.MonitoringConsolidated`
                group by YEAR.

            * Grouping `monitoring_by_co_funai`:
                `models.MonitoringConsolidated`
                group by CO_FUANI.

            * Grouping DEFAULT:
                `models.MonitoringConsolidated`
                group by CO_FUANI and YEAR.
        """
        data_grouping = self.request.GET.get('grouping', None)
        if data_grouping == "monitoring_by_co_funai_and_year":

            return models.MonitoringConsolidated.objects.values(
                'co_funai',
                'no_ti',
                'ti_nu_area_ha',
                ano=functions.ExtractYear('dt_t_um')
            ).annotate(
                total_nu_area_ha=Sum("nu_area_ha"),
                quantity_polygons=Count(
                    "no_estagio", output_field=FloatField()
                ),
                cr_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="CR")
                ),
                dg_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="DG")
                ),
                dr_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="DR")
                ),
                ff_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="FF")
                )
            ).order_by("ano")
        elif data_grouping == "monitoring_by_year":
            print("--------------2----------->>>>>>>>>---------")
            # import pdb; pdb.set_trace()

            querysett = models.MonitoringConsolidated.objects.values(
                ano=functions.ExtractYear('dt_t_um')
            ).annotate(
                total_nu_area_ha=Sum("nu_area_ha"),
                quantity_polygons=Count(
                    "no_estagio",
                    output_field=FloatField()),
                cr_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="CR")
                ),
                dg_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="DG")
                ),
                dr_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="DR")
                ),
                ff_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="FF")
                ),
                cr_nu_area_perc=F('cr_nu_area_ha') / F('ti_nu_area_ha') * Value(100, output_field=DecimalField(max_digits=3, decimal_places=3)),
                dg_nu_area_perc=F('dg_nu_area_ha') / F('ti_nu_area_ha') * Value(100, output_field=DecimalField(max_digits=3, decimal_places=3)),
                dr_nu_area_perc=F('dr_nu_area_ha') / F('ti_nu_area_ha') * Value(100, output_field=DecimalField(max_digits=3, decimal_places=3)),
                ff_nu_area_perc=F('ff_nu_area_ha') / F('ti_nu_area_ha') * Value(100, output_field=DecimalField(max_digits=3, decimal_places=3))
            ).order_by("ano")
            import pdb; pdb.set_trace()

            return querysett
        elif data_grouping == "monitoring_by_co_funai":

            querysett = models.MonitoringConsolidated.objects.values(
                'co_funai',
                'no_ti',
                'ti_nu_area_ha'
            ).annotate(
                total_nu_area_ha=Sum("nu_area_ha"),
                quantity_polygons=Count(
                    "no_estagio",
                    output_field=FloatField()
                ),
                cr_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="CR")
                ),
                dg_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="DG")
                ),
                dr_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="DR")
                ),
                ff_nu_area_ha=Sum(
                    "nu_area_ha",
                    filter=Q(no_estagio__exact="FF")
                ),
                cr_nu_area_perc=F('cr_nu_area_ha') / F('ti_nu_area_ha') * Value(
                    100, output_field=DecimalField(max_digits=3, decimal_places=3)),
                dg_nu_area_perc=F('dg_nu_area_ha') / F('ti_nu_area_ha') * Value(
                    100, output_field=DecimalField(max_digits=3, decimal_places=3)),
                dr_nu_area_perc=F('dr_nu_area_ha') / F('ti_nu_area_ha') * Value(
                    100, output_field=DecimalField(max_digits=3, decimal_places=3)),
                ff_nu_area_perc=F('ff_nu_area_ha') / F('ti_nu_area_ha') * Value(
                    100, output_field=DecimalField(max_digits=3, decimal_places=3))
            ).order_by("no_ti")

            return querysett
        return models.MonitoringConsolidated.objects.values(
            'co_funai',
            'no_ti',
            'dt_t_um',
            'ti_nu_area_ha'
        ).annotate(
            total_nu_area_ha=Sum("nu_area_ha"),
            quantity_polygons=Count(
                "no_estagio",
                output_field=FloatField()
            ),
            cr_nu_area_ha=Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="CR")
            ),
            dg_nu_area_ha=Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="DG")
            ),
            dr_nu_area_ha=Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="DR")
            ),
            ff_nu_area_ha=Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="FF")
            )
        ).order_by("dt_t_um")
