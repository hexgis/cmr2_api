from django.db.models import Sum, Count

from land_use import (
    models,
    serializers,
    filters as land_use_filters
)

from django_filters import rest_framework
from rest_framework_gis import filters as gis_filters
from rest_framework import(
    generics,
    permissions,
    response,
    status
)


class AuthModelMixIn:
    """Default Authentication for land_use views."""
    permission_classes = (permissions.AllowAny,)


class LandUseView(AuthModelMixIn, generics.ListAPIView):
    """Returns the list of `models.LandUseClasses` spatial data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseSerializer
    bbox_filter_field = 'geom'
    filterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class LandUseDetailView(AuthModelMixIn, generics.RetrieveAPIView):
    """Returns detailed data for a queried element of `models.LandUseClasses` data.

    Filters:
        * id (int): filtering request poligon identifier.
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseDetailSerializer
    lookup_field = 'id'


class LandUseYearsView(AuthModelMixIn, generics.ListAPIView):
    """Return list of years that have land use mapping for filters applied of 
    `models.LandUseClasses` data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.LandUseClasses.objects.distinct('nu_ano')
    serializer_class = serializers.LandUseYearsSerializer
    bbox_filter_field = 'geom'
    filterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class LandUseTableView(AuthModelMixIn, generics.ListAPIView):
    """Returns list data without geometry from 'models.LandUseClasses' data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseTableSerializer
    bbox_filter_field = 'geom'
    filterset_class = land_use_filters.LandUseClassesFilter
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )


class LandUseCrView(generics.ListAPIView):
    serializer_class_one = serializers.LandUseCrSerializer
    serializer_class_two = serializers.LandUseToCompareSerializer
    
    def get(self, request, *args, **kwargs):
        """
        This view compares two land use tables:
        - The first query is performed on `LandUseVmRegionalCoordnation`, distinct by the 'cr_co_cr' field.
        - The second query is performed on `LandUseClasses`, distinct by the 'co_cr' field.
        - After obtaining data from both tables, a filter is applied to return only the data
          where the 'co_cr' field in the first dataset matches the 'co_cr' field in the second dataset.
        - The filtered data is then returned in the response.
        """
        try:
            query_one = models.LandUseVmRegionalCoordnation.objects.distinct('cr_co_cr')
            query_two = models.LandUseClasses.objects.distinct('co_cr')

            data_one = self.serializer_class_one(query_one, many=True).data
            data_two = self.serializer_class_two(query_two, many=True).data

            filtered_data = [
                item for item in data_one if any(
                    str(item['co_cr']) == str(data['co_cr']) for data in data_two
                )
            ]
            
            formated_objects = [
                {
                    'no_regiao': item['no_regiao'],
                    'ds_cr': item["ds_cr"].replace("COORDENACAO REGIONAL ", ""),
                    "co_cr": item["co_cr"]
                }
                for item in filtered_data
            ]

            return response.Response(formated_objects)

        except Exception as e:
            """
            If any error occurs during the query, serialization, or filtering process, 
            the exception will be caught and a 500 Internal Server Error response will be returned.
            """
            return response.Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LandUseTiView(generics.ListAPIView):
    serializer_class_one = serializers.LandUseTiSerializer
    serializer_class_two = serializers.LandUseToCompareSerializer

    def get_queryset(self):
        """
        This method is required by ListAPIView but is not used because we're overriding `get`.
        """
        return models.LandUseVmRegionalCoordnation.objects.none() 

    def get(self, request, *args, **kwargs):
        """
        This view compares two land use datasets and filters based on the 'co_cr' parameter:
        - The first query retrieves distinct 'ti_co_funai' from `LandUseVmRegionalCoordnation`.
        - The second query retrieves distinct 'co_funai' from `LandUseClasses`.
        - After fetching the data, a filter is applied to match 'co_funai' between the two datasets.
        - Additionally, if the 'co_cr' parameter is provided, the queryset is further filtered.
        """
        try:
            co_cr_param = self.request.query_params.get('co_cr')

            query_one = models.LandUseVmRegionalCoordnation.objects.distinct('ti_co_funai')
            query_two = models.LandUseClasses.objects.distinct('co_funai')

            data_one = self.serializer_class_one(query_one, many=True).data
            data_two = self.serializer_class_two(query_two, many=True).data

            filtered_data = [
                item for item in data_one if any(
                    str(item['co_funai']) == str(data['co_funai']) for data in data_two
                )
            ]

            if co_cr_param:

                query_one = query_one.filter(cr_co_cr=co_cr_param).distinct('ti_co_funai')
                data_one = self.serializer_class_one(query_one, many=True).data
                filtered_data = data_one

            return response.Response(filtered_data)

        except Exception as e:
            """
            If any error occurs during the querying, serialization, or filtering process,
            catch the exception and return a 500 Internal Server Error response.
            """
            return response.Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LandUseStatsView(AuthModelMixIn, generics.ListAPIView):
    """Retrives `models.LandUseClasses` stats data.

    Filters:
        * co_cr (list): filtering Regional Coordination using code.
        * co_funai (list): filtering Indigenous Lands using Funai code.
        * map_year (list): filtering years mapped in land use mapping.
        * in_bbox (bbox): bounding box
            (min lon, min lat, max lon, max lat).
    """
    queryset = models.LandUseClasses.objects.all()
    serializer_class = serializers.LandUseSerializer
    filterset_class = land_use_filters.LandUseClassesFilter
    bbox_filter_field = 'geom'
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        gis_filters.InBBoxFilter,
    )

    def get(self, request):
        """Get method to return stats for land_use APP.

        Returns sums for area_ha, area_km2 and registry.

        Args:
            request (Requests.request): Request data.

        Returns:
            response.Response: django rest_framework.Response.response api response data.
        """
        data = self.filter_queryset(self.queryset).aggregate(
            area_ha=Sum('nu_area_ha'),
            area_km2=Sum('nu_area_km2'),
            total=Count('id')
        )
        return response.Response(data, status=status.HTTP_200_OK)
