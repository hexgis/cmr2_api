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
            'co_funai',
            'st_disponivel',
            'st_excluido',
            'nu_ano',
            'dt_cadastro',
            'dt_atualizacao',
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
            'usuario_id',
            'st_disponivel',
            'st_excluido',
            'dt_cadastro',
            'dt_atualizacao',
            'co_funai',
            'id_tipo',
            'no_extensao',
            'no_ti',
            'co_cr',
            'ds_cr',
            'dt_documento',
            'nu_ano',
            'nu_ano_mapa',
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