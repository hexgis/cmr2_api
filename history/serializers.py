from django.contrib.admin.models import LogEntry
from rest_framework import serializers
from user.models import User


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
