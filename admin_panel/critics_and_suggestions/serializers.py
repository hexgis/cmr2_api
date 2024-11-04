# serializers.py
from rest_framework import serializers
from .models import Ticket, TicketStatus, TicketFunctionality, TicketAnalysisHistory, TicketAttachment, TicketStatusAttachment
from django.contrib.auth.models import User
from django.utils import timezone

class TicketFunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFunctionality
        fields = ['id', 'func_name']

class TicketSerializer(serializers.ModelSerializer):
    functionality = TicketFunctionalitySerializer(read_only=True)
    functionality_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketFunctionality.objects.all(),
        source='functionality',
        write_only=True
    )
    requesting = serializers.StringRelatedField(read_only=True)
    solicitation_name = serializers.CharField(source='get_solicitation_type_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'code', 'solicitation_type', 'solicitation_name', 'functionality', 'functionality_id',
            'requesting', 'subject', 'description', 'opened_in', 'complexity_code'
        ]
        read_only_fields = ['code', 'opened_in']

    def create(self, validated_data):
        ticket = Ticket.objects.create(**validated_data)

        TicketStatus.objects.create(
            ticket=ticket,
            status_category=TicketStatus.StatusCategory.NAO_ANALISADO,
        )

        return ticket

class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ['file']

class TicketStatusAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatusAttachment
        fields = ['file']


class TicketStatusSerializer(serializers.ModelSerializer):
    status_category_name = serializers.CharField(source='get_status_category_display', read_only=True)
    sub_status_name = serializers.CharField(source='get_sub_status_display', read_only=True)
    priority_name = serializers.CharField(source='get_priority_code_display', read_only=True)
    
    ticket = serializers.StringRelatedField(read_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        source='ticket',
        write_only=True
    )
    analyzed_by = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = TicketStatus
        fields = [
            'id', 'status_category_name', 'sub_status_name',
            'priority_code', 'priority_name', 'ticket', 'ticket_id', 'analyzed_by',
            'analyzed_in', 'status_attachments'
        ]
        read_only_fields = ['analyzed_in']
    
    def validate(self, data):
        # Validar compatibilidade entre status_category e sub_status
        status_category = data.get('status_category', self.instance.status_category if self.instance else None)
        sub_status = data.get('sub_status', self.instance.sub_status if self.instance else None)

        if status_category == TicketStatus.StatusCategory.EM_ANDAMENTO and sub_status not in [
            TicketStatus.SubStatus.AGUARDANDO_GESTOR, TicketStatus.SubStatus.EM_DESENVOLVIMENTO
        ]:
            raise serializers.ValidationError("O sub-status selecionado não é válido para a categoria 'Em Andamento'.")
        
        if status_category == TicketStatus.StatusCategory.CONCLUIDO and sub_status not in [
            TicketStatus.SubStatus.CONCLUIDO, TicketStatus.SubStatus.EM_TESTE
        ]:
            raise serializers.ValidationError("O sub-status selecionado não é válido para a categoria 'Concluído'.")
        
        if status_category == TicketStatus.StatusCategory.RECUSADO and sub_status not in [
            TicketStatus.SubStatus.INVIAVEL, TicketStatus.SubStatus.INDEFERIDO
        ]:
            raise serializers.ValidationError("O sub-status selecionado não é válido para a categoria 'Recusado'.")

        return data

    # def create(self, validated_data):
    #     ticket_status = TicketStatus.objects.create(**validated_data)

    #     return ticket_status

    # def create(self, validated_data):
    #     attachments = validated_data.pop('attachments', [])
    #     ticket = Ticket.objects.create(**validated_data)

    #     for attachment in attachments:
    #         TicketAttachment.objects.create(ticket=ticket, file=attachment)

    #     TicketStatus.objects.create(
    #         ticket=ticket,
    #         status_code=TicketStatus.StatusCategory.NAO_ANALISADO, 
    #     )

    #     return ticket

class TicketAnalysisHistorySerializer(serializers.ModelSerializer):
    
    analyzed_update_formatted = serializers.SerializerMethodField()
    
    def get_analyzed_update_formatted(self, obj):
        if obj.analyzed_update:
            return timezone.localtime(obj.analyzed_update).strftime('%d/%m/%Y %H:%M:%S')
        return None
    
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

    # status_name = serializers.CharField(source='get_status_category_display', read_only=True)
    sub_status_name = serializers.CharField(source='get_sub_status_display', read_only=True)
    

    class Meta:
        model = TicketAnalysisHistory
        fields = ['id', 'comment', 'author', 'author_id', 'ticket', 'ticket_id', 'sub_status', 'sub_status_name', 'analyzed_update_formatted']
        
