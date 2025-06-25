# Built-in
import os
import json
import logging

# Django
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from user.models import Role


# Third-party
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Project-specific
from permission.mixins import Auth, Public
from utils.gen_xslx import generate_excel
from .models import (
    Ticket, TicketStatus, TicketAnalysisHistory,
    TicketStatusAttachment, TicketAttachment
)
from .serializers import (
    TicketStatusSerializer, TicketSerializer,
    TicketAttachmentSerializer, TicketStatusChoicesSerializer
)
from .validators import validate_ticket_choices
from emails.ticket_user import send_email_ticket_to_user
from emails.ticket_admins import send_email_ticket_to_admins

logger = logging.getLogger(__name__)


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


class TicketListCreateView(Auth, APIView):

    def get(self, request):
        """
        List all tickets for the authenticated user.

        If the user is a staff member, all tickets are listed.
        Otherwise, only tickets created by the requesting user are listed.

        Args: 
            request: The HTTP request object.

        Returns:
            Response: A response containing the list of tickets in serialized form.
        """
        if request.user.is_staff:
            tickets = Ticket.objects.all().order_by('-opened_in')
        else:
            tickets = Ticket.objects.filter(requesting=request.user)

        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new ticket.

        Args:
            request: The HTTP request object containing ticket data and attachments.

        Returns:
            Response: A response containing the created ticket data or error messages.
        """
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save(requesting=request.user)

            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                attachment_serializer = TicketAttachmentSerializer(data={
                    'file_path': attachment,
                    'name_file': attachment.name
                })
                if attachment_serializer.is_valid():
                    TicketAttachment.objects.create(
                        ticket=ticket, file_path=attachment)
                else:
                    return Response({'error': attachment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_ticket_choices(ticket)
            except ValidationError as e:
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(Auth, APIView):

    def get_object(self, pk, user):
        """
        Retrieves a ticket based on the user's authentication and ticket ID.

        Args:
            pk: The primary key of the ticket.
            user: The authenticated user requesting the ticket.

        Returns:
            Ticket or None: The ticket if found, otherwise None.
        """
        try:
            if user.is_staff:
                return Ticket.objects.get(pk=pk)
            return Ticket.objects.get(pk=pk, requesting=user)
        except Ticket.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieves and returns ticket details for the authenticated user.

        Args:
            request: The HTTP request object.
            pk: The primary key of the ticket to retrieve.

        Returns:
            Response: The ticket details in serialized form, or an error if not found.
        """
        ticket = self.get_object(pk, request.user)
        if ticket is None:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketStatusView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAdminUser]

    def validate_attachment_extensions(self, attachment):
        """
        Validates the file extension of a single attachment.

        Args:
            attachment: The file attachment to check.

        Returns:
            str or None: The filename if invalid, else None.
        """
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        ext = os.path.splitext(attachment.name)[1].lower()
        if ext not in valid_extensions:
            return attachment.name
        return None

    def validate_attachments(self, attachments):
        """
        Validates the attachments received in the request.

        Args:
            attachments: List of attachment files.

        Raises:
            ValidationError: If any attachment has an invalid extension.
        """
        invalid_attachments = [
            attachment.name for attachment in attachments if self.validate_attachment_extensions(attachment)]
        if invalid_attachments:
            raise ValidationError({'invalid_files': invalid_attachments})

    def handle_attachments(self, instance, attachments, ticket_history):
        """
        Processes and saves attachments related to the ticket status.

        Args:
            instance: The TicketStatus instance to associate the attachments with.
            attachments: List of attachment files.
            ticket_history: The associated ticket history.
        """
        for attachment in attachments:
            TicketStatusAttachment.objects.create(
                ticket_status=instance, ticket_history=ticket_history, file_path=attachment)

    def patch(self, request, ticket_id=None):
        """
        Updates the ticket status and creates a history entry.

        Args:
            request: The HTTP request containing the data.
            ticket_id: The ID of the ticket to update.

        Returns:
            Response: A response indicating success or failure.
        """
        try:
            ticket = Ticket.objects.get(code=ticket_id)
            instance = TicketStatus.objects.get(ticket_id=ticket_id)

            send_email_ticket_to_admins(
                ticket
            )

            data = request.data.copy()
            instance.analyzed_by = request.user
            instance.analyzed_in = timezone.now()

            # Process the `ticket_status` field
            ticket_status = data.get('ticket_status')
            if ticket_status:
                if isinstance(ticket_status, list):
                    ticket_status = ticket_status[0]
                try:
                    ticket_status_data = json.loads(ticket_status)
                    if 'formated_info' in ticket_status_data:
                        formated_info = ticket_status_data.pop('formated_info')
                        data['due_on'] = ticket_status_data.get('due_on')
                        data['status_category'] = formated_info.get(
                            'status_category_display', '')
                        data['priority_code'] = formated_info.get(
                            'priority_display')
                except json.JSONDecodeError:
                    raise ValidationError(
                        {'error': 'Invalid JSON format in ticket_status'})

            instance.solicitation_type_temp = data.get("solicitation_type", "")
            instance.complexity_code_temp = data.get("complexity_code", "")
            instance.ticket_code = ticket_id

            serializer = TicketStatusSerializer(
                instance, data=data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(
                analyzed_by=request.user, analyzed_in=timezone.now())

            # Create history entry
            comment = request.data.get('comment', '')
            ticket_history = TicketAnalysisHistory.objects.create(
                ticket=ticket,
                author=request.user,
                comment=comment
            )

            # Validate and handle attachments
            attachments = request.FILES.getlist('attachments')
            if attachments:
                self.validate_attachments(attachments)
                self.handle_attachments(instance, attachments, ticket_history)

            return Response({'status': 'ticket analyzed and history updated'}, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        except TicketStatus.DoesNotExist:
            return Response({'error': 'Ticket status not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, ticket_id=None):
        """
        Retrieves the details of a specific ticket status or lists all ticket statuses.

        Args:
            request: The HTTP request object.
            ticket_id: The ID of the ticket status to retrieve (optional).

        Returns:
            Response: The ticket status data or a list of all ticket statuses.
        """
        if ticket_id:
            try:
                instance = TicketStatus.objects.get(ticket_id=ticket_id)
                serializer = TicketStatusSerializer(
                    instance, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except TicketStatus.DoesNotExist:
                return Response({'error': 'Ticket status not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = TicketStatus.objects.all()
        serializer = TicketStatusSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenXLSXView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Generates an Excel report for the provided list of ticket IDs.

        Args:
            request: The HTTP request object containing the list of ticket IDs.

        Returns:
            Response: An Excel file as an attachment or an error message if validation fails.
        """
        ticket_ids = request.data.get("ticket_ids", [])

        if not ticket_ids:
            return Response(
                {"error": "É necessário fornecer uma lista de IDs de tickets."},
                status=status.HTTP_400_BAD_REQUEST
            )

        tickets = Ticket.objects.filter(code__in=ticket_ids)
        if not tickets.exists():
            return Response(
                {"error": "Nenhum ticket encontrado com os IDs fornecidos."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TicketSerializer(tickets, many=True)

        # Define column headers for the Excel file
        title = [
            "Código", "Tipo da Solicitação", "Funcionalidade", "Assunto", "Descrição", "Solicitante",
            "Criado em", "Status", "Prioridade", "Analisado por", "Previsão de Entrega"
        ]

        # Prepare data for each ticket to be written in the Excel file
        data = []
        for ticket in serializer.data:
            data.append([
                ticket["code"],
                ticket["solicitation_name"],
                ticket["functionality"]["func_name"],
                ticket["subject"],
                strip_tags(ticket["description"]),
                ticket["requesting"],
                ticket["opened_in_formatted"],
                ticket['ticket_status']['formated_info']['status_category_display'],
                ticket['ticket_status']['formated_info']['priority_display'],
                ticket['ticket_status']['user_info']['analyzer'],
                ticket['ticket_status']['formated_info']['formated_due_on'],
            ])

        # Generate the Excel file and prepare the response
        xlsx_file = generate_excel(title, data)

        # Set up the response to return the Excel file as an attachment
        response = HttpResponse(
            xlsx_file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="tickets_report.xlsx"'

        return response


class GetChoices(APIView):

    def get(self, request):
        serializer = TicketStatusChoicesSerializer(instance={})
        return Response(serializer.data)


class SendTicketEmailView(Auth, APIView):
    def post(self, request):
        try:
            data = request.data.copy()
            ticket = Ticket.objects.get(code=data['ticket_id'])

            send_email_ticket_to_user(
                ticket,
                data
            )

            return Response({'status': 'Emails sent successfully!'}, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            logger.warning("Ticket não encontrado: %s", data.get('ticket_id'))
            return Response({'error': 'Ticket not found.'}, status=status.HTTP_404_NOT_FOUND)

        except FileNotFoundError:
            logger.warning("Template de e-mail não encontrado.")
            return Response({'error': 'Email template not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.warning("Erro ao enviar e-mails: %s", str(e))
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadDocument(APIView):
    def get(self, request, filename):
        filepath = os.path.join(
            settings.MEDIA_ROOT, 'attachments', 'critcs_and_suggestions', 'answer', filename)
        try:
            return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
        except FileNotFoundError:
            return Response({'error': 'Arquivo não encontrado'}, status=404)


class DownloadManual(APIView):
    def get(self, request):
        filepath = os.path.join(
            settings.DOC_TEMPLATE_DIR, 'Manual_MVP_CMR2_2025.pdf')
        try:
            return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='Manual_MVP_CMR2_2025.pdf')
        except FileNotFoundError:
            return Response({'error': 'Arquivo não encontrado'}, status=404)
