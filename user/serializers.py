from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers
from django.conf import settings


from permission import models as permission_models
from user import models


class UserSettingsSerializer(serializers.ModelSerializer):
    """Class to serialize User Data adding settings as related field."""

    class Meta:
        """Meta class for `serializer.UserSerializer`."""

        model = models.User
        fields = (
            'avatar_blob',
            'avatar',
            'dark_mode_active',
        )

    def update(
        self,
        instance: models.User,
        validated_data: dict
    ) -> models.User:
        """Update an existing user instance.

        Args:
            instance (models.User): Instance of User.
            validated_data (dict): User data.

        Returns:
            models.User: User instance.
        """

        instance = super().update(instance, validated_data)

        data = self.context['request'].data.get('settings') or ''

        if 'avatar' in data and not data['avatar']:
            instance.avatar = None
            instance.avatar_blob = None

        instance.save()

        return instance


class SimpleRoleSerializer(serializers.ModelSerializer):
    """SimpleRoleSerializer serializer class."""

    class Meta:
        """Meta class for SimpleRolesSerializer."""

        model = models.Role
        fields = ('id', 'name')


class SimpleGroupSerializer(serializers.ModelSerializer):
    """SimpleGroupSerializer serializer class."""

    class Meta:
        """Meta class for SimpleGroupsSerializer."""

        model = models.Group
        fields = ('id', 'name')


class SimpleUserSerializer(serializers.ModelSerializer):
    """SimpleUserSerializer serializer class."""

    class Meta:
        """Meta class for SimpleUsersSerializer."""

        model = models.User
        fields = ('id', 'username')


class UserSerializer(serializers.ModelSerializer):
    """Class to serialize User Data adding settings as related field."""

    settings = serializers.SerializerMethodField()

    components = serializers.SerializerMethodField()

    roles = SimpleRoleSerializer(many=True, read_only=True)

    institution = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    institution_id = serializers.SlugRelatedField(
        source='institution',
        slug_field='id',
        read_only=True
    )

    def get_settings(self, obj: models.User) -> str:
        """Get user settings.
        Args:
            obj (User): User instance.

        Returns:
            str: User settings serialized data.
        """

        serializer = UserSettingsSerializer(obj)
        return serializer.data

    def get_components(self, obj: models.User) -> str:
        """Get user settings.
        Args:
            obj (User): User instance.

        Returns:
            str: User settings serialized data.
        """

        components = {component[0] for component in settings.COMPONENT_LIST}

        if obj.is_admin:
            data = components
        if obj.is_authenticated:
            queryset = permission_models.ComponentPermission.objects.filter(
                groups__roles__users=obj.id
            ).values_list('components', flat=True)
            data = list(set(item for sublist in queryset for item in sublist))
        else:
            return {component: False for component in components}

        return {component: (component in data) for component in components}

    def create(self, validated_data: dict) -> models.User:
        """Create a new user instance.

        Args:
            validated_data (dict): User data.

        Returns:
            User: User instance.
        """

        data = self.context['request'].data

        if 'settings' in data:
            validated_data.update(data['settings'])

        user = models.User.objects.create_user(**validated_data)

        if 'password' in data:
            user.set_password(data['password'])

        if 'institution' in data:
            user.institution = models.Institution.objects.get_or_create(
                name=data['institution']
            )[0]

        if 'roles' in data:
            user.roles.clear()
            user.roles.set(data['roles'])

        user.save()

        return user

    def update(
        self,
        instance: models.User,
        validated_data: dict
    ) -> models.User:
        """Update an existing user instance.

        Args:
            instance (User): User instance.
            validated_data (dict): User data.

        Returns:
            User: User instance.
        """

        data = self.context['request'].data

        if 'settings' in data:
            validated_data.update(data['settings'])

        instance = super().update(instance, validated_data)

        if 'password' in data:
            instance.set_password(data['password'])

        if 'institution' in data:
            instance.institution = models.Institution.objects.get_or_create(
                name=data['institution']
            )[0]

        if 'roles' in data:
            instance.roles.clear()
            instance.roles.set(data['roles'])

        instance.save()

        return instance

    class Meta:
        """Meta class for `serializer.UserSerializer`."""

        model = models.User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'settings',
            'roles',
            'institution',
            'institution_id',
            'is_superuser',
            'is_staff',
            'components'
        )


class UserUploadedFileSerializer(serializers.ModelSerializer):
    """Class to serialize `models.UserUploadedFile` model data."""

    class Meta:
        """Meta class for `UserUploadedFileSerializer`."""

        model = models.UserUploadedFile
        fields = '__all__'


class UserUploadedFileGeometryListSerializer(gis_serializers.GeoFeatureModelSerializer):
    """
    Class to serialize `UserUploadedFileGeometry` geo model data.
    """
    class Meta:
        model = models.UserUploadedFileGeometry
        geo_field = 'geom'
        id_field = False
        fields = (
            'id',
            'user_uploaded',
            'geom',
            'properties',
        )


class UserUploadedFileGeometryDetailSerializer(serializers.ModelSerializer):
    """Class to serialize `models.UserUploadedFileGeometry` model data."""

    def to_representation(self, instance: models.UserUploadedFileGeometry):
        """Returns instance.properties model data.

        Args:
            instance (models.UserUploadedFileGeometry): model data.

        Returns:
            dict: properties
        """

        return instance.properties

    class Meta:
        """Meta class for `UserUploadedFileGeometryDetailSerializer`."""

        model = models.UserUploadedFileGeometry
        fields = ('id',)


class InstitutionSerializer(serializers.ModelSerializer):
    """UsageInstitutionSerializer serializer class."""

    class Meta:
        """Meta class for UsageInstitutionsSerializer."""

        model = models.Institution
        fields = (
            'id',
            'name',
        )


class RoleSerializer(serializers.ModelSerializer):
    """RoleSerializer serializer class."""

    users = SimpleUserSerializer(many=True, read_only=True)
    groups = SimpleGroupSerializer(many=True, read_only=True)

    def create(self, validated_data: dict) -> models.Role:
        """Create a new role instance.

        Args:
            validated_data (dict): Role data.

        Returns:
            Role: Role instance.
        """

        obj = models.Role.objects.create(
            name=validated_data['name'],
            description=validated_data['description']
        )

        data = self.context['request'].data

        if 'groups' in data:
            obj.groups.clear()
            obj.groups.set(data['groups'])

        if 'users' in data:
            obj.users.clear()
            obj.users.set(data['users'])

        return obj

    def update(
        self,
        instance: models.Role,
        validated_data: dict
    ) -> models.Role:
        """Update an existing role instance.

        Args:
            instance (Role): Role instance.
            validated_data (dict): Role data.

        Returns:
            Role: Role instance.
        """

        instance = super().update(instance, validated_data)

        data = self.context['request'].data

        if 'groups' in data:
            instance.groups.clear()
            instance.groups.set(data['groups'])

        if 'users' in data:
            instance.users.clear()
            instance.users.set(data['users'])

        return instance

    class Meta:
        """Meta class for RolesSerializer."""

        model = models.Role
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """GroupSerializer serializer class."""

    roles = SimpleRoleSerializer(many=True, read_only=True)

    def create(self, validated_data: dict) -> models.Group:
        """Create a new group instance.

        Args:
            validated_data (dict): Group data.

        Returns:
            Group: Group instance.
        """

        obj = models.Group.objects.create(
            name=validated_data['name'],
            description=validated_data['description']
        )

        data = self.context['request'].data

        if 'roles' in data:
            obj.roles.clear()
            obj.roles.set(data['roles'])

        if 'layer_permissions' in data:
            obj.layer_permissions.clear()
            obj.layer_permissions.set(data['layer_permissions'])

        if 'component_permissions' in data and data['component_permissions']:
            obj.component_permissions.clear()
            obj.component_permissions.set(data['component_permissions'])

        return obj

    def update(
        self,
        instance: models.Group,
        validated_data: dict
    ) -> models.Group:
        """Update an existing group instance.

        Args:
            instance (Group): Group instance.
            validated_data (dict): Group data.

        Returns:
            Group: Group instance.
        """

        instance = super().update(instance, validated_data)

        data = self.context['request'].data

        if 'roles' in data:
            instance.roles.clear()
            instance.roles.set(data['roles'])

        if 'layer_permissions' in data:
            instance.layer_permissions.clear()
            instance.layer_permissions.set(data['layer_permissions'])

        if 'component_permissions' in data and data['component_permissions']:
            instance.component_permissions.clear()
            instance.component_permissions.set(data['component_permissions'])

        return instance

    class Meta:
        """Meta class for GroupsSerializer."""

        model = models.Group
        fields = '__all__'


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AccessRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for AccessRequest model data.
    """

    class Meta:
        model = models.AccessRequest
        fields = [
            'id',
            'name',
            'email',
            'department',
            'user_siape_registration',
            'coordinator_name',
            'coordinator_email',
            'coordinator_department',
            'coordinator_siape_registration',
            'attachment',
            'status',
            'dt_solicitation',
            'dt_approvement',
        ]
        read_only_fields = ['status', 'dt_solicitation', 'dt_approvement']

    def create(self, validated_data):
        """
        Overriding create to ensure any new request defaults to status=False.
        """
        validated_data['status'] = False
        return super().create(validated_data)
