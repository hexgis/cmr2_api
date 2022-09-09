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
            'id_action',
            'no_action',
            'action_type',
            'description',
        )


class UsuarioSerializers(serializers.ModelSerializer):
    """Serializer to return the user who entered the `models.Usuario` data."""

    class Meta:
        """Meta class for `UsuarioSerializers` serializer."""
        model = models.UsersCMR
        fields = (
            'id_user',
            'first_name',
        )


class MapasUsoOcupacaoSoloSerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocumentalDocs` data.

    Data only for the action category linked to USO_OCUPAÇÃO_DO_SOLO
    """

    usercmr_id = UsuarioSerializers()
    action_id = ActionListSerializers()

    class Meta:
        """Meta class for `MapasUsoOcupacaoSoloSerializers` serializer."""
        model = models.DocumentalDocs
        fields = (
            'id_document',
            'path_document',
            'no_document',
            'st_available',
            'st_excluded',
            'co_funai',
            'no_ti',
            'co_cr',
            'ds_cr',
            'dt_registration',
            'dt_update',
            'nu_year',
            'nu_year_map',
            'action_id',
            'usercmr_id',
        )

    def to_representation(self, instance):
        """Method to return in `MapasUsoOcupacaoSoloSerializers` the full URL
        to download the documents in `models.DocumentalDocs`.

        Returns:
            str: url to document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(
            settings.DOCUMENTOS, instance.path_document)
        return url_document


class DocumentosTISerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocumentalDocs` data.

    Data only for the action category linked to DOCUMENTAL_TI.
    """

    usercmr_id = UsuarioSerializers()
    action_id = ActionListSerializers()

    class Meta:
        """Meta class for `DocumentosTISerializers` serializer."""
        model = models.DocumentalDocs
        fields = (
            'id_document',
            'path_document',
            'no_document',
            'no_extension',
            'st_available',
            'st_excluded',
            'co_funai',
            'no_ti',
            'co_cr',
            'ds_cr',
            'dt_registration',
            'dt_update',
            'dt_document',
            'action_id',
            'usercmr_id',
        )

    def to_representation(self, instance):
        """Method to return in `DocumentosTISerializers` the full URL to
        download the documents in `models.DocumentalDocs`.

        Returns:
            str: url to document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(
            settings.DOCUMENTOS, instance.path_document)
        return url_document
