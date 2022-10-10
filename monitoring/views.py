from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_gis import filters as gis_filters

from rest_framework import (
    generics,
    response,
    permissions,
    status
)

from django.db.models import (Sum, OuterRef, Subquery, F, Case, When, Value, Count)

from monitoring import (
    serializers,
    models,
    filters as monitoring_filters
)

from django.db.models import (Sum, OuterRef, Subquery, F, Q, Case, When, Value, Count, FloatField, functions)


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
    """"""

    filterset_class = monitoring_filters.MonitoringConsolidatedStatsFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )
    agrupar_por_ANO = True
    agrupar_por_CO_FUNAI = True

    def get_serializer_class(self):
        # agrupar_ti = self.request.GET.get('agrupar_ti', None) \
        #     if self.request.GET.get('agrupar_ti') == 'true' else None
        # agrupar_ano = self.request.GET.get('agrupar_ano', None) \
        #     if self.request.GET.get('agrupar_ano') == 'true' else None

        
        if self.agrupar_por_CO_FUNAI and self.agrupar_por_ANO:
            return serializers.ConsultaMonitoramentoTIAgrupadoAnoTISerializer
        elif self.agrupar_por_CO_FUNAI:
            return serializers.ConsultaMonitoramentoTIAgrupadoSerializer
        elif self.agrupar_por_ANO:
            return serializers.ConsultaMonitoramentoTIAgrupadoAnoSerializer
        else:
            return serializers.ConsultaMonitoramentoTerraIndigenaSerializer
        
            
        
        # return serializers.xptoSerializers

    def get_queryset(self):
        # agrupar_ti = True \
        #     if self.request.GET.get('agrupar_ti') == 'true' else None
        # agrupar_ano = True \
        #     if self.request.GET.get('agrupar_ano') == 'true' else None
        # # ordem =  ??
        # if agrupar_ti or agrupar_ano:
        #     if agrupar_ti and agrupar_ano:
        #         queryset = queryset \
        #             .values('co_funai', 'no_ti', 'ti_nu_area_ha', ano=ExtractYear('dt_t_um')) \
        #             .order_by(ordem, 'ano')
        #     elif agrupar_ti:
        #         queryset = queryset \
        #             .values('co_funai', 'no_ti', 'ti_nu_area_ha') \
        #             .order_by(ordem)
        #     elif agrupar_ano:
        #         queryset = queryset \
        #             .values(ano=ExtractYear('dt_t_um')) \
        #             .order_by('ano')
        # else:
        #     queryset = queryset \
        #         .values('co_funai', 'dt_t_um', 'no_ti', 'ti_nu_area_ha') \
        #         .order_by(ordem, 'dt_t_um')

        # queryset = queryset.annotate(
        #     total_nu_area_ha=Sum('nu_area_ha'),
        #     cr_nu_area_ha=Sum(Case(
        #         When(no_estagio='CR', then=F('nu_area_ha')), default=Value(0))),
        #     dg_nu_area_ha=Sum(Case(
        #         When(no_estagio='DG', then=F('nu_area_ha')), default=Value(0))),
        #     dr_nu_area_ha=Sum(Case(
        #         When(no_estagio='DR', then=F('nu_area_ha')), default=Value(0))),
        #     ff_nu_area_ha=Sum(Case(
        #         When(no_estagio='FF', then=F('nu_area_ha')), default=Value(0)))
        # )
        # return queryset

        # import pdb; pdb.set_trace()

        if self.agrupar_por_CO_FUNAI and self.agrupar_por_ANO:
            return models.MonitoringConsolidatedStats.objects.values('co_funai','no_ti','ti_nu_area_ha',ano=functions.ExtractYear('dt_t_um')).annotate(total_nu_area_ha = Sum("nu_area_ha"),quantity_polygons= Count("no_estagio",output_field=FloatField()), cr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="CR")), dg_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DG")),dr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DR")), ff_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="FF"))).order_by("ano")
        elif self.agrupar_por_ANO:
            return models.MonitoringConsolidatedStats.objects.values(ano=functions.ExtractYear('dt_t_um')).annotate(total_nu_area_ha = Sum("nu_area_ha"),quantity_polygons= Count("no_estagio",output_field=FloatField()), cr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="CR")), dg_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DG")),dr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DR")), ff_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="FF"))).order_by("ano")
        elif self.agrupar_por_CO_FUNAI:
            return models.MonitoringConsolidatedStats.objects.values('co_funai','no_ti','ti_nu_area_ha').annotate(total_nu_area_ha = Sum("nu_area_ha"),quantity_polygons= Count("no_estagio",output_field=FloatField()), cr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="CR")), dg_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DG")),dr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DR")), ff_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="FF"))).order_by("no_ti")
        else:#agrupar_por_DIA
            return models.MonitoringConsolidatedStats.objects.values('co_funai','no_ti', 'dt_t_um','ti_nu_area_ha',).annotate(total_nu_area_ha = Sum("nu_area_ha"),quantity_polygons= Count("no_estagio",output_field=FloatField()), cr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="CR")), dg_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DG")),dr_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="DR")), ff_nu_area_ha= Sum("nu_area_ha",filter=Q(no_estagio__exact="FF"))).order_by("dt_t_um")
        # dia=functions.ExtractDay('dt_t_um')
        # return models.MonitoringConsolidatedStats.objects.values().filter(id__gte=303789959, id__lte=303789962)
        # return models.MonitoringConsolidatedStats.objects.values().filter(id__gte=303789959, id__lte=303789982)
