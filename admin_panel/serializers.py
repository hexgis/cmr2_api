from rest_framework import serializers
from .models import Ticket, TicketStatus, TicketFunctionality, TicketAnalysisHistory, TicketAttachment, TicketStatusAttachment
from django.utils import timezone
from django.contrib.auth import get_user_model
from .validators import validate_status_and_substatus, format_datetime, validate_complexity, format_date


class TicketFunctionalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFunctionality
        fields = ['id', 'func_name']


class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ['file_path', 'name_file']


class TicketStatusAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatusAttachment
        fields = ['file_path', 'name_file']


class TicketStatusSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    formated_info = serializers.SerializerMethodField()

    class Meta:
        model = TicketStatus
        fields = [
            'id', 'due_on', 'user_info', 'formated_info',
            'status_category', 'sub_status', 'priority_code'
        ]
        read_only_fields = ['analyzed_in']

    def get_user_info(self, obj):
        """Consolida informações sobre o usuário que analisou o ticket."""
        return {
            "analyzer": obj.analyzed_by.username if obj.analyzed_by else None,
            "analyzer_email": obj.analyzed_by.email if obj.analyzed_by else None,
        }

    def get_formated_info(self, obj):
        return {
            "analyzed_in_formatted": format_datetime(obj.analyzed_in) if obj.analyzed_in else None,
            "formated_due_on": format_date(obj.due_on) if obj.due_on else None,
            "status_category_display": obj.get_status_category_display(),
            "sub_status_display": obj.get_sub_status_display(),
            "priority_display": obj.get_priority_code_display(),
        }

    def validate(self, data):
        cleaned_data = {key: value for key, value in data.items() if value not in [
            None, 'null', '']}

        status_category = cleaned_data.get(
            'status_category', self.instance.status_category if self.instance else None)
        sub_status = cleaned_data.get(
            'sub_status', self.instance.sub_status if self.instance else None)
        current_status = self.instance.status_category if self.instance else None
        current_substatus = self.instance.sub_status if self.instance else None

        validate_status_and_substatus(
            status_category, sub_status, current_status, current_substatus)
        return data

    def update(self, instance, data):
        cleaned_data = {key: value for key, value in data.items() if value not in [
            None, 'null', '']}
        for key, value in cleaned_data.items():
            setattr(instance, key, value)

        if instance.solicitation_type_temp not in [None, 'null', '']:
            # Atualizar o Ticket no banco de dados
            Ticket.objects.filter(code=instance.ticket_code).update(
                solicitation_type=instance.solicitation_type_temp)

        if instance.complexity_code_temp not in [None, 'null', '']:
            # Atualizar o Ticket no banco de dados
            Ticket.objects.filter(code=instance.ticket_code).update(
                complexity_code=instance.complexity_code_temp)

        instance.analyzed_by = data.get(
            'analyzed_by', self.context['request'].user)
        instance.analyzed_in = timezone.now()
        return super().update(instance, cleaned_data)

    def create(self, data):
        """Método de criação, onde garantimos a limpeza dos dados antes de salvar."""
        cleaned_data = {key: value for key, value in data.items() if value not in [
            None, 'null', '']}
        instance = self.Meta.model.objects.create(**cleaned_data)
        return instance

    def to_representation(self, instance):
        """Oculta os campos `status_category` e `sub_status` no retorno."""
        representation = super().to_representation(instance)
        representation.pop('status_category', None)
        representation.pop('sub_status', None)
        representation.pop('priority_code', None)
        return representation


class TicketAnalysisHistorySerializer(serializers.ModelSerializer):
    User = get_user_model()

    analyzed_update_formatted = serializers.SerializerMethodField()
    status_history_attachments = TicketStatusAttachmentSerializer(
        many=True, read_only=True)

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
    )

    sub_status_name = serializers.CharField(
        source='get_sub_status_display', read_only=True)

    class Meta:
        model = TicketAnalysisHistory
        fields = [
            'id', 'comment', 'author', 'author_id', 'ticket', 'ticket_id', 'sub_status_name',
            'analyzed_update_formatted', 'status_history_attachments'
        ]


class TicketSerializer(serializers.ModelSerializer):
    functionality = serializers.PrimaryKeyRelatedField(
        queryset=TicketFunctionality.objects.all(), required=False)
    requesting = serializers.StringRelatedField(read_only=True)
    requesting_email = serializers.SerializerMethodField(read_only=True)

    complexity_code = serializers.IntegerField(
        required=False, allow_null=True, validators=[validate_complexity])
    solicitation_type = serializers.CharField(required=False, allow_null=True)

    solicitation_name = serializers.CharField(
        source='get_solicitation_type_display', read_only=True)

    # usando aspas para o DRF definir o serializer de forma atrasada
    ticket_status = serializers.SerializerMethodField()
    ticket_analysis_history = serializers.SerializerMethodField()

    opened_in_formatted = serializers.SerializerMethodField()

    def get_opened_in_formatted(self, obj):
        return format_datetime(obj.opened_in)

    status_category = serializers.ChoiceField(
        choices=TicketStatus.StatusCategory.choices,
        write_only=True,
        required=False,
        default=TicketStatus.StatusCategory.NAO_ANALISADO,
    )

    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.functionality:
            representation['functionality'] = TicketFunctionalitySerializer(
                instance.functionality).data
        return representation

    class Meta:
        model = Ticket
        fields = [
            'code', 'solicitation_type',  'solicitation_name', 'complexity_code', 'functionality', 'requesting', 'requesting_email', 'subject', 'description', 'opened_in_formatted',  'attachments', 'ticket_status', 'ticket_analysis_history', 'status_category'
        ]
        read_only_fields = ['code', 'opened_in']

    def create(self, validated_data):
        print(validated_data)
        status_category = validated_data.pop(
            'status_category', TicketStatus.StatusCategory.NAO_ANALISADO)

        ticket = Ticket.objects.create(**validated_data)

        TicketStatus.objects.create(
            ticket=ticket,
            status_category=status_category,
        )

        return ticket

    def get_ticket_status(self, obj):
        try:
            ticket_status = TicketStatus.objects.get(ticket=obj)
            return TicketStatusSerializer(ticket_status).data
        except TicketStatus.DoesNotExist:
            return None

    def get_ticket_analysis_history(self, obj):
        analysis_history = TicketAnalysisHistory.objects.filter(
            ticket=obj).order_by('-analyzed_update')

        return TicketAnalysisHistorySerializer(analysis_history, many=True).data

    def get_requesting_email(self, obj):
        return obj.requesting.email if obj.requesting else None


class TicketStatusChoicesSerializer(serializers.Serializer):
    status_category = serializers.SerializerMethodField()
    sub_status = serializers.SerializerMethodField()
    priority_code = serializers.SerializerMethodField()
    complexity = serializers.SerializerMethodField()
    solicitation_type = serializers.SerializerMethodField()
    functionality = serializers.SerializerMethodField()

    def get_functionality(self, obj):
        functionality = TicketFunctionality.objects.all().order_by('id')
        return TicketFunctionalitySerializer(functionality, many=True).data

    def get_status_category(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in TicketStatus.StatusCategory.choices]

    def get_sub_status(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in TicketStatus.SubStatus.choices]

    def get_priority_code(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in TicketStatus.Priority.choices]

    def get_complexity(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in Ticket.Complexity.choices]

    def get_solicitation_type(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in Ticket.SolicitationType.choices]
