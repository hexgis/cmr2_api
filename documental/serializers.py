from rest_framework import serializers

from documental import models
from django.conf import settings


class ActionListSerializers(serializers.ModelSerializer):
    """Serializer for return list actions `models.Action` data."""
    class Meta:
        """Meta class for `ActionListSerializers` serializer."""
        model = models.Action
        fields = (
            'id',
            'no_acao',
        )


class UsuarioSerializers(serializers.ModelSerializer):
    """Serializer to return user who entered the document `models.Usuario` data.
    """
    class Meta:
        """Meta class for `UsuarioSerializers` serializer."""
        model = models.Usuario
        fields = (
            'id',
            'first_name',
        )


class MapasUsoOcupacaoSoloSerializers(serializers.ModelSerializer):
    """Serializer to return datas to action category USO_OCUPAÇÃO_DO_SOLO to
    `models.DocumentalDocs` data.
    """
    usuario_id = UsuarioSerializers()
    acao_id = ActionListSerializers()
    class Meta:
        """Meta class for `MapasUsoOcupacaoSoloSerializers` serializer."""
        model = models.DocumentalDocs
        fields = (
            'id',
            'path_documento',
            'no_documento',
            'co_funai',
            'st_disponivel',
            'st_excluido',
            'nu_ano',
            'dt_cadastro',
            'dt_atualizacao',
            'nu_ano_mapa',
            'acao_id',
            'usuario_id',
        )
    
    def to_representation(self, instance):
        """Method to return in `DocumentosTISerializers` the full URL to
        download the documents in `models.DocumentalDocs`  
                
        Returns:
            url_document -> str
        """
        url_document = super().to_representation(instance)
        url_document['url_doc'] = settings.DOCUMENTOS + instance.path_documento
        return url_document


