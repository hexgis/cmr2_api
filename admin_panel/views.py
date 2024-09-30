from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from user_profile import serializers as UserSerializers
from user_profile import models as UserModels

from admin_panel import serializers, models

class UsersInstitutionsView(APIView):
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = UserModels.UserData.objects.filter(user=user) 
        serializer = UserSerializers.UserDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        institution_id = request.data.get('instituicao')
        try:
            institution_instance = models.Institutions.objects.get(id=institution_id)
        except models.Institutions.DoesNotExist:
            return Response("detail: Institution not found", status=status.HTTP_404_NOT_FOUND)

        try:
            data = UserModels.UserData(
                user=user,
                institution=institution_instance
            )
            data.save()
            return Response('detail: User Institution successfully registered', status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response('detail: User has already registered an institution', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'Error: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        institution_id = request.data.get('instituicao')
        try:
            institution_instance = models.Institutions.objects.get(id=institution_id)
        except models.Institutions.DoesNotExist:
            return Response("detail: Institution not found", status=status.HTTP_404_NOT_FOUND)
        
        try:
            user_data = UserModels.UserData.objects.get(user=user)
            user_data.institution = institution_instance
            user_data.save()
            return Response('detail: User institution successfully updated', status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("detail: User institution data not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f'Error {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InstitutionsView(APIView):

    TYPE_MAPPING = {
        1: 'Funai Sede',
        2: 'Em Branco',
        3: 'Outros',
    }

    def get(self, request, *args, **kwargs):
        queryset = models.Institutions.objects.all()
        serializer = serializers.InstitutionSerailizer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        institution_name = request.data.get('name')
        institution_type_code = request.data.get('type')  # Recebe 1, 2, ou 3

        if not institution_name or institution_type_code is None:
            return Response("detail: name and type can't be empty ", status=status.HTTP_204_NO_CONTENT)

        institution_type = self.TYPE_MAPPING.get(institution_type_code)

        if institution_type is None:
            return Response("detail: Invalid type!", status=status.HTTP_400_BAD_REQUEST)

        try:
            data = models.Institutions(
                name=institution_name,
                type=institution_type
            )
            data.save()
            return Response('detail: Institution successfully registered', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f'Error {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        institution_id = kwargs.get('id')
        institution_name = request.data.get('name')
        institution_type_code = request.data.get('type')
        allowed_types = self.TYPE_MAPPING

        try:
            institution = models.Institutions.objects.get(id=institution_id)
        except models.Institutions.DoesNotExist:
            return Response("detail: Institution not found", status=status.HTTP_404_NOT_FOUND)

        if institution_name:
            institution.name = institution_name

        if institution_type_code:
            institution_type = allowed_types.get(institution_type_code)
            if institution_type is None:
                return Response("detail: Invalid type!", status=status.HTTP_400_BAD_REQUEST)
            institution.type = institution_type
        
        try:
            institution.save()
            return Response('detail: Institution successfully updated', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Error {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



