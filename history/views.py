from django.contrib.admin.models import LogEntry
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import LogEntrySerializer
from .models import UserRoleChange, UserChangeHistory
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()


class LogEntryViewSet(ReadOnlyModelViewSet):
    serializer_class = LogEntrySerializer
    queryset = LogEntry.objects.all().order_by('-action_time')

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            return UserChangeHistory.objects.filter(user_id=user_id).order_by('-changed_at')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{
            'id': change.id,
            'alterado_por': change.changed_by.username,
            'action_time': change.changed_at,
            'username': change.new_username,
            'email': change.new_email,
            'institution': change.new_institution
        } for change in queryset]
        return Response(data)


class UserRoleChangeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for retrieving user role change history."""
    queryset = UserRoleChange.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return (UserRoleChange.objects.filter(user_id=user_id)
                    .select_related('changed_by', 'role', 'user')
                    .order_by('-changed_at'))
        return UserRoleChange.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{
            'id': change.id,
            'changed_by': change.changed_by.username,
            'changed_at': change.changed_at.strftime('%d/%m/%Y %H:%M:%S'),
            'action': 'Removido' if change.action == 'removed' else 'Adicionado',
            'role': change.role.name,
        } for change in queryset]
        return Response(data)
