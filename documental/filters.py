from django_filters import rest_framework

from documental import models

class NumberInFilter(
    rest_framework.BaseInFilter,
    rest_framework.NumberFilter
):
    """Base class used for creating IN lookup filters to filter numbers."""
    pass
    
    
class CharInFilter(
    rest_framework.BaseInFilter,
    rest_framework.CharFilter
):    
    """Base class used for creating IN lookup filters to filter characters."""
    pass
