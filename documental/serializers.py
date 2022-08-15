from rest_framework import serializers

import urllib
from django.conf import settings

from documental import models


class ActionListSerializers(serializers.ModelSerializer):
    """Serializer for return list actions `models.DocsAction` data."""

    class Meta:
        """Meta class for `ActionListSerializers` serializer."""
        model = models.DocsAction
        fields = (
            'id',
            'no_acao',
            'descricao',
        )


class UsuarioSerializers(serializers.ModelSerializer):
    """Serializer to return the user who entered the `models.Usuario` data."""

    class Meta:
        """Meta class for `UsuarioSerializers` serializer."""
        model = models.Usuario
        fields = (
            'id',
            'first_name',
        )

class DocumentSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.Document
        fields = ('file', 'data', 'uploaded_at', 'action')


class MapasUsoOcupacaoSoloSerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocumentalDocs` data.

    Data only for the action category linked to USO_OCUPAÇÃO_DO_SOLO
    """

    usuario_id = UsuarioSerializers()
    id_acao = ActionListSerializers()

    class Meta:
        """Meta class for `MapasUsoOcupacaoSoloSerializers` serializer."""
        model = models.DocumentalDocs
        fields = (
            'id',
            'path_documento',
            'no_documento',
            'st_disponivel',
            'st_excluido',
            'co_funai',
            'no_ti',
            'co_cr',
            'ds_cr',
            'dt_cadastro',
            'dt_atualizacao',
            'nu_ano',
            'nu_ano_mapa',
            'id_acao',
            'usuario_id',
        )
    
    def to_representation(self, instance):
        """Method to return in `MapasUsoOcupacaoSoloSerializers` the full URL
        to download the documents in `models.DocumentalDocs`.
                
        Returns:
            str: url to document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(settings.DOCUMENTOS, instance.path_documento)     
        return url_document


class DocumentosTISerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocumentalDocs` data.

    Data only for the action category linked to DOCUMENTAL_TI.
    """

    usuario_id = UsuarioSerializers()
    id_acao = ActionListSerializers()

    class Meta:
        """Meta class for `DocumentosTISerializers` serializer."""
        model = models.DocumentalDocs
        fields = (
            'id',
            'path_documento',
            'no_documento',
            'no_extensao',
            'st_disponivel',
            'st_excluido',
            'co_funai',
            'no_ti',
            'co_cr',
            'ds_cr',
            'dt_cadastro',
            'dt_atualizacao',
            'dt_documento',
            'id_acao',
            'usuario_id',
        )

    def to_representation(self, instance):
        """Method to return in `DocumentosTISerializers` the full URL to
        download the documents in `models.DocumentalDocs`.
                
        Returns:
            str: url to document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(settings.DOCUMENTOS, instance.path_documento)
        return url_document