from django.contrib.admin.models import LogEntry
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import LogEntrySerializer, UserChangeHistorySerializer, UserRoleChangeSerializer  # updated import
from .models import UserRoleChange, UserChangeHistory
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()


class LogEntryViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for retrieving system log entries and user change history.

    Behavior:
    - If a 'user_id' query parameter is provided, returns the change history
      for that specific user from the UserChangeHistory model.
    - Otherwise, returns the full list of LogEntry records ordered by action time.

    Responses:
    - Uses serializers to return a representation of user changes,
      including fields such as who made the change, when it occurred,
      and both old and new values for the user's attributes.

    Query Parameters:
    - user_id (optional): Filter the logs to show only the change history for a specific user.

    Note:
    - This viewset is read-only and does not allow creation, update, or deletion of records.
    """

    queryset = LogEntry.objects.all().order_by(
        '-action_time')  # add back queryset attribute

    def get_serializer_class(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return UserChangeHistorySerializer
        return LogEntrySerializer

    def get_queryset(self):
        queryset = LogEntry.objects.all().order_by('-action_time')
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return UserChangeHistory.objects.filter(user_id=user_id).order_by('-changed_at')
        return queryset


class UserRoleChangeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving the history of user role changes.

    Behavior:
    - If a 'user_id' query parameter is provided, returns the role change
      history for the specified user, ordered by the date of change (descending).
    - If no 'user_id' is provided, returns an empty queryset.

    Responses:
    - Custom `list` method returns a simplified list of role change entries,
      including who made the change, when it occurred, the action performed
      (Added or Removed), and the role affected.

    Query Parameters:
    - user_id (optional): Filter the results to changes related to a specific user.

    Note:
    - This is a read-only endpoint; creation, update, and deletion are not allowed.
    """
    queryset = UserRoleChange.objects.all()  # ensure queryset attribute is present
    serializer_class = UserRoleChangeSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            return (
                UserRoleChange.objects.filter(user_id=user_id)
                .select_related('changed_by', 'role', 'user')
                .order_by('-changed_at')
            )
        return UserRoleChange.objects.none()
