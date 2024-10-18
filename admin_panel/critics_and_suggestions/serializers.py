# serializers.py
from rest_framework import serializers
from .models import Ticket, TicketStatus, TicketFunctionality, TicketAnalysisHistory, TicketAttachment, TicketStatusAttachment
from django.contrib.auth.models import User

class TicketFunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFunctionality
        fields = ['id', 'func_name']

class TicketSerializer(serializers.ModelSerializer):

    attachments = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    functionality = TicketFunctionalitySerializer(read_only=True)
    functionality_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketFunctionality.objects.all(),
        source='functionality',
        write_only=True
    )
    requesting = serializers.StringRelatedField(read_only=True)

    solicitation_name = serializers.CharField(source='get_solicitation_type_code_display', read_only=True)
    class Meta:
        model = Ticket
        fields = [
            'code', 'solicitation_type_code', 'solicitation_name' , 'functionality', 'functionality_id',
            'requesting', 'subject', 'description', 'attachments', 'opened_in', 'complexity_code'
        ]
        read_only_fields = ['code', 'opened_in']

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', [])
        ticket = Ticket.objects.create(**validated_data)

        for attachment in attachments:
            TicketAttachment.objects.create(ticket=ticket, file=attachment)

        TicketStatus.objects.create(
            ticket=ticket,
            status_code=TicketStatus.Status.NAO_ANALISADO, 
        )

        return ticket

class TicketStatusSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='get_status_code_display', read_only=True)
    priority_name = serializers.CharField(source='get_priority_code_display', read_only=True)
    
    ticket = serializers.StringRelatedField(read_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        source='ticket',
        write_only=True
    )
    analyzed_by = serializers.StringRelatedField(read_only=True)

    status_attachments = serializers.ListField(
        child=serializers.FileField(),
        write_only=True
    )

    class Meta:
        model = TicketStatus
        fields = [
            'id', 'status_code', 'status_name', 'priority_code', 'priority_name',
            'ticket', 'ticket_id', 'analyzed_by',
            'analyzed_in', 'status_attachments'
        ]
        read_only_fields = ['analyzed_in']

    def create(self, validated_data):
        status_attachments = validated_data.pop('status_attachments', [])
        ticket_status = TicketStatus.objects.create(**validated_data)

        for attachment in status_attachments:
            TicketStatusAttachment.objects.create(ticket_status=ticket_status, file=attachment)

        return ticket_status


class TicketAnalysisHistorySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True
    )
    ticket = serializers.StringRelatedField(read_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        source='ticket',
        write_only=True
    )

    status_name = serializers.CharField(source='get_status_code_display', read_only=True)

    class Meta:
        model = TicketAnalysisHistory
        fields = ['id', 'comment', 'author', 'author_id', 'ticket', 'ticket_id', 'status_code', 'status_name', 'analyzed_update']
