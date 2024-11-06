from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket, TicketStatus, TicketAnalysisHistory, TicketStatusAttachment, TicketAttachment
from .serializers import (
    TicketSerializer, TicketStatusSerializer, TicketAnalysisHistorySerializer, TicketAttachmentSerializer
)
from .validators import validate_ticket_choices, validate_due_on

from django.core.exceptions import ValidationError
from django.utils import timezone

import os

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a ticket to view it.
    Everyone can create tickets.
    """

    def has_object_permission(self, request, view, obj):
        return obj.requesting == request.user

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return request.user.is_authenticated

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(requesting=self.request.user)

    def perform_create(self, serializer):
        ticket = serializer.save(requesting=self.request.user)

        attachments = self.request.FILES.getlist('attachments')

        for attachment in attachments:
            attachment_serializer = TicketAttachmentSerializer(data={'file': attachment})
            if attachment_serializer.is_valid():
                TicketAttachment.objects.create(ticket=ticket, file=attachment)
                print("Attachment Saved")
            else:
                print(f"Attachment not saved due to errors: {attachment_serializer.errors}")
        try:
            validate_ticket_choices(ticket)
            
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketAnalysisHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer
    lookup_field = 'ticket_id'
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, ticket_id=None): 
        try:
            ticket = Ticket.objects.get(code=ticket_id)
            instance = self.get_object()
            
            attachments = self.request.FILES.getlist('attachments')
            invalid_attachments = []
            valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']

            for attachment in attachments:
                ext = os.path.splitext(attachment.name)[1]
                if ext.lower() not in valid_extensions:
                    invalid_attachments.append(attachment.name)
                    
            if invalid_attachments:
                return Response(
                    {'invalid_files': invalid_attachments},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            for attachment in attachments:
                TicketStatusAttachment.objects.create(ticket_status=instance, file=attachment)
               
            instance.analyzed_by = request.user
            instance.analyzed_in = timezone.now()
            
            status_category = request.data.get('status_category', instance.status_category)
            sub_status = request.data.get('sub_status', instance.sub_status)
            priority_code = request.data.get('priority_code', instance.priority_code)
            due_on = request.data.get('due_on', instance.due_on)
            
            try:
                converted_due_on = validate_due_on(due_on)
            except ValidationError as e:
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data.copy()
            data['due_on'] = converted_due_on

            instance.status_category = status_category
            instance.sub_status = sub_status
            instance.priority_code = int(priority_code)
            
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            comment = request.data.get('comment', '')
            TicketAnalysisHistory.objects.create(
                ticket=ticket,
                author=request.user,
                comment=comment,
                sub_status=instance.sub_status
            )

            return Response({'status': 'ticket analyzed and history updated'}, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TicketAnalysisHistoryViewSet(viewsets.ModelViewSet):
    queryset = TicketAnalysisHistory.objects.all().order_by('-analyzed_update')
    serializer_class = TicketAnalysisHistorySerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, pk=None):
        ticket_id = pk
        analysis_history = TicketAnalysisHistory.objects.filter(ticket_id=ticket_id).order_by('-analyzed_update')

        if not analysis_history.exists():
            return Response({'detail': 'No analysis history found for this ticket.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(analysis_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

