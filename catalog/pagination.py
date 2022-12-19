from django.conf import settings
from rest_framework_gis.pagination import GeoJsonPagination


class CatalogoGeoJsonPagination(GeoJsonPagination):
    """
    Geojson pagination for page size
    Get from settings PAGE_SIZE or default will be 10
    """
    page_size_query_param = 'page_size'

    if hasattr(settings, 'PAGE_SIZE') and settings.PAGE_SIZE:
        page_size = settings.PAGE_SIZE
    else:
        page_size = 20
