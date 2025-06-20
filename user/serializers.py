from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from emails.new_user import send_new_user
from emails.new_user_ad import send_new_user_ad

from permission import models as permission_models
from user import models
from django.utils.translation import gettext_lazy as _


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
        # Create new reset code with one week expiration
        reset_code = models.PasswordResetCode.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(days=7)
        )

        if data['email'].endswith('@funai.gov.br'):
            send_new_user_ad(reset_code, data['email'])
        else:
            send_new_user(reset_code, data['email'])

        if 'password' in data:
            user.set_password(data['password'])

        if 'institution_id' in data:
            try:
                institution = models.Institution.objects.get(
                    id=data['institution_id'])
                user.institution = institution
            except models.Institution.DoesNotExist:
                raise serializers.ValidationError({
                    'institution': 'Instituição com este ID não existe.'
                })

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

        if 'institution_id' in data:
            try:
                institution = models.Institution.objects.get(
                    id=data['institution_id']
                )
                instance.institution = institution
            except models.Institution.DoesNotExist:
                raise serializers.ValidationError({
                    'institution_id': 'Instituição com este ID não existe.'
                })

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
            'is_active',
            'is_superuser',
            'is_staff',
            'components',
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
            'institution_type',
        )


class RoleSerializer(serializers.ModelSerializer):
    users = SimpleUserSerializer(many=True, read_only=True)
    groups = SimpleGroupSerializer(many=True, read_only=True)
    associated_groups = serializers.PrimaryKeyRelatedField(
        queryset=models.Group.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    associated_users = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    def create(self, validated_data: dict) -> models.Role:
        associated_groups = validated_data.pop('associated_groups', [])
        associated_users = validated_data.pop('associated_users', [])

        obj = models.Role.objects.create(
            name=validated_data['name'],
            description=validated_data['description']
        )

        if associated_groups:
            obj.groups.set(associated_groups)
        if associated_users:
            obj.users.set(associated_users)

        return obj

    def update(self, instance, validated_data):
        associated_groups = validated_data.pop('associated_groups', None)
        associated_users = validated_data.pop('associated_users', None)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if associated_groups is not None:
            instance.groups.set(associated_groups)
        if associated_users is not None:
            instance.users.set(associated_users)

        return instance

    class Meta:
        model = models.Role
        fields = ['id', 'name', 'description', 'groups', 'users',
                  'associated_groups', 'associated_users']


class GroupSerializer(serializers.ModelSerializer):
    """GroupSerializer serializer class."""

    roles = SimpleRoleSerializer(many=True, read_only=True)
    layer_permissions = serializers.SerializerMethodField()
    component_permissions = serializers.SerializerMethodField()

    def get_layer_permissions(self, obj):
        """Retrieve the names of the layer permissions."""
        return [
            {"id": permission.id, "name": permission.name,
                "description": permission.description}
            for permission in obj.layer_permissions.all()
        ]

    def get_component_permissions(self, obj):
        """Retrieve the names of the component permissions."""
        return [
            {"id": component.id, "name": component.name}
            for component in obj.component_permissions.all()
        ]

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
            'created_at',
            'reviewed_at',
            'reviewed_by',
            'denied_details',
        ]
        read_only_fields = ['status', 'created_at', 'reviewed_at']

    def create(self, validated_data):
        """
        Overriding create to ensure any new request defaults to status=False.
        """
        validated_data['status'] = models.AccessRequest.StatusType.PENDENTE
        return super().create(validated_data)


class AccessRequestDetailSerializer(serializers.ModelSerializer):
    """
     Serializer to return detailed information about an AccessRequest.
     Includes status details and formatted fields.
     """
    """
    Serializer to return detailed information about an AccessRequest.
    Includes status details and formatted fields.
    """

    created_at_formatted = serializers.SerializerMethodField()
    reviewed_at_formatted = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    denied_details = serializers.SerializerMethodField()

    class Meta:
        model = models.AccessRequest
        fields = [
            "id",
            "name",
            "email",
            "department",
            "user_siape_registration",
            "coordinator_name",
            "coordinator_email",
            "coordinator_department",
            "coordinator_siape_registration",
            "attachment",
            "created_at_formatted",
            "status_name",
            "reviewed_at_formatted",
            "reviewed_by_name",
            "denied_details",
        ]

    def get_created_at_formatted(self, obj):
        """
        Formats the solicitation date.
        """
        return obj.created_at.strftime("%d/%m/%Y %H:%M:%S") if obj.created_at else None

    def get_reviewed_at_formatted(self, obj):
        """
        Formats the reviewed date from AccessRequestStatus.
        """
        return obj.reviewed_at.strftime("%d/%m/%Y %H:%M:%S") if obj.reviewed_at else None

    def get_status_name(self, obj):
        """
        Gets the name of the status from AccessRequestStatus.
        """
        return obj.get_status_display()

    def get_reviewed_by_name(self, obj):
        """
        Gets the name of the reviewer from AccessRequestStatus.
        """
        return obj.reviewed_by.username if obj.reviewed_by else None

    def get_denied_details(self, obj):
        """
        Gets the denied details from AccessRequestStatus.
        """
        return obj.denied_details


class PasswordResetConfirmSerializer(serializers.Serializer):
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": _("Passwords do not match.")
            })

        try:
            reset_code = models.PasswordResetCode.objects.get(
                code=data['code'])
        except models.PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({
                "code": _("Invalid or expired reset code.")
            })

        if reset_code.is_expired():
            raise serializers.ValidationError({
                "code": _("Reset code has expired.")
            })

        # Armazena para uso posterior no método save()
        self.reset_code = reset_code
        return data

    def save(self):
        new_password = self.validated_data['new_password']
        user = self.reset_code.user
        user.set_password(new_password)
        user.save()
        self.reset_code.delete()
        return user
