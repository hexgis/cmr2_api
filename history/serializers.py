from django.contrib.admin.models import LogEntry
from rest_framework import serializers
from user.models import User
from .models import UserChangeHistory, UserRoleChange


class LogEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the LogEntry model, used to represent system activity logs.

    Custom fields:
    - user: Username associated with the action, if available.
    - user_institution: Name of the institution linked to the user, if applicable.
    - user_is_active: Indicates whether the user was active at the time of the action.
    - action_time: Formatted date and time of the action.
    - action_flag_display: Human-readable description of the action (Added, Changed, Deleted).

    Model fields:
    - id: Log entry identifier.
    - action_flag: Numeric code of the action (1 = added, 2 = changed, 3 = deleted).
    - change_message: Descriptive message of the change.
    - content_type: Type of the affected content.
    - object_id: ID of the affected object.
    - object_repr: Text representation of the affected object.
    """
    user = serializers.SerializerMethodField()
    user_institution = serializers.SerializerMethodField()
    user_is_active = serializers.SerializerMethodField()
    action_time = serializers.DateTimeField(format="%d/%m/%Y às %H:%M")
    action_flag_display = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = [
            'id',
            'user',
            'user_institution',
            'user_is_active',
            'action_time',
            'action_flag',
            'action_flag_display',
            'change_message',
            'content_type',
            'object_id',
            'object_repr'
        ]

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def get_user_institution(self, obj):
        if obj.user and hasattr(obj.user, 'institution') and obj.user.institution:
            return obj.user.institution.name
        return None

    def get_user_is_active(self, obj):
        if obj.user:
            return obj.user.is_active
        return None

    def get_action_flag_display(self, obj):
        if obj.action_flag == 1:
            return "Adicionado"
        elif obj.action_flag == 2:
            return "Alterado"
        elif obj.action_flag == 3:
            return "Excluído"
        return "Desconhecido"


class UserChangeHistorySerializer(serializers.ModelSerializer):
    alterado_por = serializers.CharField(
        source='changed_by.username', read_only=True)
    action_time = serializers.DateTimeField(
        source='changed_at', format='%d/%m/%Y %H:%M:%S', read_only=True)
    username = serializers.CharField(source='new_username', read_only=True)
    email = serializers.CharField(source='new_email', read_only=True)
    institution = serializers.CharField(
        source='new_institution', read_only=True)
    is_active = serializers.BooleanField(
        source='new_is_active', read_only=True)
    old_is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserChangeHistory
        fields = [
            'id',
            'alterado_por',
            'action_time',
            'username',
            'email',
            'institution',
            'is_active',
            'old_is_active'
        ]


class UserRoleChangeSerializer(serializers.ModelSerializer):
    changed_by = serializers.CharField(
        source='changed_by.username', read_only=True)
    changed_at = serializers.DateTimeField(
        format='%d/%m/%Y %H:%M:%S', read_only=True)
    action = serializers.SerializerMethodField()
    role = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = UserRoleChange
        fields = [
            'id',
            'changed_by',
            'changed_at',
            'action',
            'role',
        ]

    def get_action(self, obj):
        return 'Removido' if obj.action == 'removed' else 'Adicionado'
