from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime

from dashboard import models

class DashboardDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the DashboardData model to format and customize the data.

    Attributes:
    - user: A custom field to include the username instead of user ID.
    - last_date_login: A custom field to format the date and time of the last login.

    Methods:
    - get_user: Returns the username associated with the DashboardData object.
    - get_last_date_login: Formats the last login date and time.
    """

    # Custom field to format the last login date and time
    last_date_login = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the DashboardDataSerializer.
        
        Specifies the model and fields to be serialized.

        Attributes:
        - model: The model class to be serialized (DashboardData).
        - fields: List of fields to be included in the serialized output.
        """
        model = models.DashboardData
        fields = ['id','last_date_login', 'location', 'ip', 'type_device', 'browser']
    
    def get_last_date_login(self, obj):
        """
        Formats the last date and time of login for the DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The formatted date and time of the last login in 'dd/mm/yyyy HH:MM:SS' format.
        """
        # Convert date to the desired format
        return obj.last_date_login.strftime('%d/%m/%Y %H:%M:%S') if obj.last_date_login else None
