from rest_framework.serializers import ModelSerializer
from authorization import models


class UserPermssionsSerializer(ModelSerializer):
    
    class Meta:
        model = models.PermissionsList
        fields = '__all__'