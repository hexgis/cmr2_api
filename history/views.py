from django.contrib.admin.models import LogEntry
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import LogEntrySerializer
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from .models import UserRoleChange
from rest_framework import viewsets
from rest_framework.response import Response


class LogEntryViewSet(ReadOnlyModelViewSet):
    serializer_class = LogEntrySerializer
    queryset = LogEntry.objects.all().order_by('-action_time')

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtro por usuário
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(object_id=user_id)

        # Filtro por data
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(action_time__gte=start_date)

        return queryset


class UserRoleChangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserRoleChange.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return UserRoleChange.objects.filter(user_id=user_id).order_by('-changed_at')
        return UserRoleChange.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{
            'changed_by': change.changed_by.username,
            'changed_at': change.changed_at,
            'action': change.action,
            'role': change.role.name,
        } for change in queryset]
        return Response(data)
