from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Class to serialize User Data adding settings as related field."""

    sector = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `serializer.UserSerializer`."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'sector'
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
