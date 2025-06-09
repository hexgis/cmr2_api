from django.contrib.admin.models import LogEntry
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import LogEntrySerializer
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType


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
