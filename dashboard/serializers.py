from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime

from dashboard import models


class DashboardDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the DashboardData model to format and customize the data.

    Attributes:
    - user_email: A custom field to include the user's email.
    - user_username: A custom field to include the username.
    - institution_name: A custom field to include the institution name.
    - institution_acronym: A custom field to include the institution acronym.
    - institution_type: A custom field to include the institution type.
    - last_date_login: A custom field to format the date and time of the last login.

    Methods:
    - get_user_email: Returns the email associated with the DashboardData object.
    - get_user_username: Returns the username associated with the DashboardData object.
    - get_institution_name: Returns the institution name.
    - get_institution_acronym: Returns the institution acronym.
    - get_institution_type: Returns the institution type.
    - get_last_date_login: Formats the last login date and time.
    """

    # Custom fields to include user and institution data
    user_email = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()
    institution_name = serializers.SerializerMethodField()
    institution_acronym = serializers.SerializerMethodField()
    institution_type = serializers.SerializerMethodField()

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
        fields = [
            'id',
            'user_email',
            'user_username',
            'institution_name',
            'institution_acronym',
            'institution_type',
            'last_date_login',
            'location',
            'ip',
            'type_device',
            'browser',
            'latitude',
            'longitude'
        ]

    def get_user_email(self, obj):
        """
        Returns the email of the user associated with the DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The user's email or None if no user is associated.
        """
        return obj.user.email if obj.user else None

    def get_user_username(self, obj):
        """
        Returns the username of the user associated with the DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The username or None if no user is associated.
        """
        return obj.user.username if obj.user else None

    def get_institution_name(self, obj):
        """
        Returns the institution name of the user associated with the
        DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The institution name or None if no institution is associated.
        """
        if obj.user and obj.user.institution:
            return obj.user.institution.name
        return None

    def get_institution_acronym(self, obj):
        """
        Returns the institution acronym of the user associated with the
        DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The institution acronym or None if no institution is associated.
        """
        if obj.user and obj.user.institution:
            return obj.user.institution.acronym
        return None

    def get_institution_type(self, obj):
        """
        Returns the institution type of the user associated with the
        DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The institution type or None if no institution is associated.
        """
        if obj.user and obj.user.institution:
            return obj.user.institution.institution_type
        return None

    def get_last_date_login(self, obj):
        """
        Formats the last date and time of login for the DashboardData object.

        Args:
        - obj (DashboardData): The instance of the DashboardData model.

        Returns:
        - str: The formatted date and time of the last login in
               'dd/mm/yyyy' format.
        """
        # Convert date to the desired format
        if obj.last_date_login:
            return obj.last_date_login.strftime('%d/%m/%Y')
        return None
