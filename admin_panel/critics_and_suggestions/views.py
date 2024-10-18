# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket, TicketStatus, TicketFunctionality, TicketAnalysisHistory, TicketStatusAttachment
from .serializers import (
    TicketSerializer, TicketStatusSerializer,
    TicketFunctionalitySerializer, TicketAnalysisHistorySerializer
)
from .validators import validate_status_ticket_choices, validate_ticket_choices

from django.core.exceptions import ValidationError
from django.utils import timezone

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
        
        if 'annex_question' in self.request.FILES:
            ticket.annex_question = self.request.FILES['annex_question']
            ticket.save() 

        try:
            validate_ticket_choices(ticket)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, ticket_id=None, *args, **kwargs):
        try:
            ticket = Ticket.objects.get(code=ticket_id)
            instance = self.get_object()

            # Atualizando os campos necessários
            instance.analyzed_by = request.user
            instance.analyzed_in = timezone.now()

            # Obtendo e convertendo os status_code e priority_code
            status_code = request.data.get('status_code', instance.status_code)
            priority_code = request.data.get('priority_code', instance.priority_code)

            if status_code is not None:
                instance.status_code = int(status_code)

            if priority_code is not None:
                instance.priority_code = int(priority_code)

            # Validando a atualização do status
            validate_status_ticket_choices(instance)

            # Salvando as mudanças no TicketStatus
            instance.save()

            # Processando os anexos
            status_attachments = request.FILES.getlist('status_attachments')
            for attachment in status_attachments:
                TicketStatusAttachment.objects.create(ticket_status=instance, file=attachment)

            # Adicionando histórico da análise
            comment = request.data.get('comment', '')
            TicketAnalysisHistory.objects.create(
                ticket=ticket,
                author=request.user,
                comment=comment,
                status_code=instance.status_code
            )

            return Response({'status': 'ticket analyzed and history updated'}, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TicketAnalysisHistoryViewSet(viewsets.ModelViewSet):
    queryset = TicketAnalysisHistory.objects.all()
    serializer_class = TicketAnalysisHistorySerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, pk=None):
        ticket_id = pk
        analysis_history = TicketAnalysisHistory.objects.filter(ticket_id=ticket_id)

        if not analysis_history.exists():
            return Response({'detail': 'No analysis history found for this ticket.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(analysis_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
