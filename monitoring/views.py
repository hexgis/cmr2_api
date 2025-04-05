from django.db.models import Count, Sum, functions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis import filters as gis_filters
from rest_framework import (
    generics,
    permissions,
    response,
    status
)

from monitoring import filters as monitoring_filters
from monitoring import models, serializers, groupings

from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.contrib.gis.geos import Polygon
from django.db.models import Q
from rest_framework.response import Response


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
        'no_estagio').distinct('no_estagio')
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
    bbox_filter_field = 'geom'
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    filter_backends = (
        DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


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
            monitoring_by_monthyear,
            monitoring_by_co_funai_and_year,
            monitoring_by_co_funai_and_monthyear,
            monitoring_by_day or None or Any other

    Returns group by in request field grouping:
        * monitoring_by_year:
            `models.MonitoringConsolidated` group by YEAR.
            `serializers.MonitoringConsolidatedByYearSerializer`.
        * monitoring_by_monthyear:
            `models.MonitoringConsolidated` group by MONTH and YEAR.
            `serializers.MonitoringConsolidatedByMonthYearSerializer`.
        * monitoring_by_co_funai:
            `models.MonitoringConsolidated` group by CO_FUANI.
            `serializers.MonitoringConsolidatedByCoFunaiSerializer`.
        * monitoring_by_co_funai_and_year:
            `models.MonitoringConsolidated` group by CO_FUANI and YEAR.
            `serializers.MonitoringConsolidatedByCoFunaiAndYearSerializer`.
        * monitoring_by_co_funai_and_monthyear:
            `models.MonitoringConsolidated` group by CO_FUANI and MONTH and YEAR.
            `serializers.MonitoringConsolidatedByCoFunaiAndMonthYearSerializer`.
        * DEFAULT is iquals monitoring_by_day:
            Used when request is None or not metch with keys previously listed.
            `models.MonitoringConsolidated` group by CO_FUANI and YEAR.
            `serializers.MonitoringConsolidatedByDaySerializer`.
    """
    filterset_class = monitoring_filters.MonitoringConsolidatedFilter
    bbox_filter_field = 'geom'
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
            `serializers.MonitoringConsolidatedByCoFunaiAndMonthYearSerializer` or
            `serializers.MonitoringConsolidatedByCoFunaiSerializer` or
            `serializers.MonitoringConsolidatedByYearSerializer`or
            `serializers.MonitoringConsolidatedByMonthYearSerializer`or
            `serializers.MonitoringConsolidatedByDaySerializer`.
        """
        data_grouping = self.request.GET.get('grouping', None)

        if data_grouping == "monitoring_by_co_funai_and_year":
            return serializers.MonitoringConsolidatedByCoFunaiAndYearSerializer
        elif data_grouping == "monitoring_by_co_funai_and_monthyear":
            return serializers.MonitoringConsolidatedByCoFunaiAndMonthYearSerializer
        elif data_grouping == "monitoring_by_co_funai":
            return serializers.MonitoringConsolidatedByCoFunaiSerializer
        elif data_grouping == "monitoring_by_year":
            return serializers.MonitoringConsolidatedByYearSerializer
        elif data_grouping == "monitoring_by_monthyear":
            return serializers.MonitoringConsolidatedByMonthYearSerializer
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

            * Grouping `monitoring_by_co_funai_and_monthyear`:
                `models.MonitoringConsolidated`
                group by CO_FUANI and MONTH and YEAR.

            * Grouping `monitoring_by_year`:
                `models.MonitoringConsolidated`
                group by YEAR.79089.307",

            * Grouping `monitoring_by_monthyear`:
                `models.MonitoringConsolidated`
                group by MONTH and YEAR.

            * Grouping `monitoring_by_co_funai`:
                `models.MonitoringConsolidated`
                group by CO_FUANI.

            * Grouping DEFAULT:
                `models.MonitoringConsolidated`
                group by CO_FUANI and YEAR.
        """
        data_grouping = self.request.GET.get('grouping', None)
        if data_grouping == "monitoring_by_co_funai_and_year":
            queryset = models.MonitoringConsolidated.objects.values(
                'co_funai',
                'no_ti',
                'ti_nu_area_ha',
                ano=functions.ExtractYear('dt_t_um')
            )
            queryset = groupings.GroupingClassificationOfStages.absolute_number_and_percentage(
                self, queryset)

            return queryset.order_by("ano")

        elif data_grouping == "monitoring_by_co_funai_and_monthyear":
            queryset = models.MonitoringConsolidated.objects.values(
                'co_funai',
                'no_ti',
                'ti_nu_area_ha',
                mes=functions.ExtractMonth('dt_t_um'),
                ano=functions.ExtractYear('dt_t_um')
            )
            queryset = groupings.GroupingClassificationOfStages.absolute_number_and_percentage(
                self, queryset)

            return queryset.order_by("mes", "ano")

        elif data_grouping == "monitoring_by_year":
            queryset = models.MonitoringConsolidated.objects.values(
                ano=functions.ExtractYear('dt_t_um')
            )
            queryset = groupings.GroupingClassificationOfStages.absolute_number(
                self, queryset)

            return queryset.order_by("ano")

        elif data_grouping == "monitoring_by_monthyear":
            queryset = models.MonitoringConsolidated.objects.values(
                mes=functions.ExtractMonth('dt_t_um'),
                ano=functions.ExtractYear('dt_t_um')
            )
            queryset = groupings.GroupingClassificationOfStages.absolute_number(
                self, queryset)

            return queryset.order_by("mes", "ano")

        elif data_grouping == "monitoring_by_co_funai":
            queryset = models.MonitoringConsolidated.objects.values(
                'co_funai',
                'no_ti',
                'ti_nu_area_ha'
            )
            queryset = groupings.GroupingClassificationOfStages.absolute_number_and_percentage(
                self, queryset)

            return queryset.order_by("no_ti")

        else:
            queryset = models.MonitoringConsolidated.objects.values(
                'co_funai',
                'no_ti',
                'dt_t_um',
                'ti_nu_area_ha'
            )
            queryset = groupings.GroupingClassificationOfStages.absolute_number(
                self,
                queryset
            )

            return queryset.order_by("dt_t_um")


class BboxFeatureCollectionView(generics.ListAPIView):
    def post(self, request):
        # Extrair os dados do POST
        co_funai_list = request.data.get('co_funai', [])
        co_cr_list = request.data.get('co_cr', [])

        # Validar os dados
        if not co_funai_list and not co_cr_list:
            return Response(
                {"error": "Pelo menos um dos campos 'co_funai' ou 'co_cr' deve ser fornecido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter co_funai para inteiros (se necessário)
        try:
            co_funai_list = [int(co)
                             for co in co_funai_list] if co_funai_list else []
        except ValueError:
            return Response(
                {"error": "Os valores de 'co_funai' devem ser inteiros."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar a query com OR entre co_funai e co_cr
        query = Q()
        if co_funai_list:
            query |= Q(co_funai__in=co_funai_list)
        if co_cr_list:
            query |= Q(co_cr__in=co_cr_list)

        # Consultar a tabela
        try:
            wkt_array = models.MonitoringConsolidated.objects\
                .filter(query)\
                .order_by('co_funai')\
                .distinct('co_funai')

            if not wkt_array.exists():
                return Response(
                    {"error": "Nenhum dado encontrado para os filtros fornecidos."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extrair as geometrias do campo 'geom' (ajuste o nome do campo conforme necessário)
            multipolygons = [GEOSGeometry(obj.geom) for obj in wkt_array]

            if not multipolygons:
                return Response(
                    {"error": "Nenhuma geometria válida encontrada nos dados."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Unir todas as geometrias em uma única (union geral)
            merged_geometry = multipolygons[0]
            for geom in multipolygons[1:]:
                merged_geometry = merged_geometry.union(geom)

            # Obter o envelope (bbox)
            bbox = merged_geometry.extent  # retorna (xmin, ymin, xmax, ymax)

            if not bbox:
                return Response(
                    {"error": "Não foi possível calcular o bbox."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(bbox, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Erro ao processar a solicitação: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
