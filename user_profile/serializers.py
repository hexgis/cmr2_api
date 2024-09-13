from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from user_profile import models


class UserSettingsSerializer(serializers.ModelSerializer):
    """Class to serialize `models.UserSettings` model data."""

    class Meta:
        model = models.UserSettings
        fields = (
            'dark_mode_active',
            'map_zoom_buttons_visible',
            'drawer_open_on_init',
            'map_search_button_visible',
            'map_scale_visible',
            'minimap_visible',
            'map_pointer_coordinates_visible',
        )


class UserSerializer(serializers.ModelSerializer):
    """Class to serialize User Data adding settings as related field."""

    settings = UserSettingsSerializer()

    class Meta:
        """Meta class for `serializer.UserSerializer`."""

        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'settings',
        )

    def get_sector(self, obj: User) -> str:
        """Returns the sector associated with the user.

        Args:
            obj (User): User instance.

        Returns:
            str: user_sector sector name or `None`.
        """

        try:
            return obj.usersector.sector.name
        except Exception as exc:
            print(f'An exception occured while getting sector: {exc}')
            return None


class UserUploadedFileSerializer(serializers.ModelSerializer):
    """Class to serialize `models.UserUploadedFile` model data."""

    class Meta:
        """Meta class for `UserUploadedFileSerializer`."""

        model = models.UserUploadedFile
        fields = (
            'id',
            'name',
            'date_created',
            'is_active',
            'properties',
        )


class UserUploadFileDeleteSerializer(serializers.ModelSerializer):
    """Serializer class for setting user status to false."""

    def update(self, instance, validated_data):
        """Post "False" value to user uploaded file "is_active" field.

        Args:
            instance (dict): Instance of user upload file.
            validated_data (dict): Unused necessary field for update method.

        Returns:
            dict: User uploaded file instance with "is_active" field set to
                "False".
        """

        instance.is_active = False
        instance.save()
        return instance

    class Meta:
        """Meta class for `UserUploadFileDeleteSerializer`."""

        model = models.UserUploadedFile
        fields = (
            'id',
            'is_active',
        )

class UserUploadedFileGeometryListSerializer(
    gis_serializers.GeoFeatureModelSerializer
):
    """Class to serialize `models.UserUploadedFileGeometry` geo model data."""
    marker_properties = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `UserUploadedFileGeometryListSerializer`."""

        model = models.UserUploadedFileGeometry
        geo_field = 'geom'
        id_field = False
        fields = (
            'id',
            'user_uploaded',
            'geom',
            'marker_properties'
            )
        
    def get_marker_properties(self, obj):
        """Retorna apenas o campo `properties` do `UserUploadedFile`."""
        if obj.user_uploaded:
            return obj.user_uploaded.properties
        return None

class UserUploadedFileGeometryDetailSerializer(serializers.ModelSerializer):
    """Class to serialize `models.UserUploadedFileGeometry` model data."""

    def to_representation(self, instance: models.UserUploadedFileGeometry):
        """Returns properties from the related `UserUploadedFile`.

        Args:
            instance (models.UserUploadedFileGeometry): model data.

        Returns:
            dict: properties
        """
        # Acessa o campo `properties` relacionado a partir de `UserUploadedFile`
        return instance.user_uploaded.properties

    class Meta:
        """Meta class for `UserUploadedFileGeometryDetailSerializer`."""

        model = models.UserUploadedFileGeometry
        fields = (
            'id'
        )
