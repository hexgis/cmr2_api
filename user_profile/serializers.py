from django.contrib.auth.models import User

from rest_framework import serializers

from user_profile import models


class UserSettingsSerializer(serializers.ModelSerializer):
    """Class to serialize `models.UserSettings` model data."""

    class Meta:
        model = models.UserSettings
        fields = (
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


class UserUploadFileUpdateSerializer(serializers.ModelSerializer):
    """Serializer class for user update."""

    def update(self, instance, validated_data):
        """Updates name value to user uploaded file.

        Args:
            instance (dict): Instance of user upload file.
            validated_data (dict): Unused necessary field for update method.

        Returns:
            dict: User uploaded file instance with updated name field.
        """

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = models.UserUploadedFile
        fields = (
            'id',
            'name',
        )
