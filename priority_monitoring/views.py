# # from django.shortcuts import render

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import (
#     SessionAuthentication, BasicAuthentication
# )
# from django.http import HttpResponse
# from django.http import JsonResponse


# def xindex1(request):
#     return HttpResponse('<h1>lucas</h1> <h2>testando 123<h2/>')

# def xindex2(request):
#     return render(request, 'index.html')

# def valor_json (request):
#     #renderisando um objeto JSON
#     if request.method == 'GET':
#         teste = {'id':1, 'name':'LSA'}
#         return JsonResponse(teste)


###############################################################
###############################################################
###############################################################


from rest_framework import viewsets, filters
from priority_monitoring.serializers import PriorityConsolidatedSerializer
from priority_monitoring.models import PriorityConsolidated
from priority_monitoring.filters import PriorityConsolidatedFilter

from django_filters.rest_framework import DjangoFilterBackend

class PriorityConsolidatedView(viewsets.ModelViewSet):
    """Retorna todos os monitoramento prioritários"""
    queryset = PriorityConsolidated.objects.all()
    serializer_class = PriorityConsolidatedSerializer
    filterset_class = PriorityConsolidatedFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['no_cr', 'no_ti', 'ranking']
