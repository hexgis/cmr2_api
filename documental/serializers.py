from rest_framework import serializers

import urllib
from django.conf import settings

from documental import models


"""List of common fields for Serializers classes."""
list_fields_serializers_commun = [
    'file',
    'id_document',
    'path_document',
    'no_document',
    'st_available',
    'st_excluded',
    'dt_registration',
    'dt_update',
    'co_funai',
    'co_cr',
    'ds_cr',
    'no_ti',
    'action_id',
    'usercmr_id',
]


class ActionListSerializers(serializers.ModelSerializer):
    """Serializer for return list actions `models.DocsAction` data."""

    class Meta:
        """Meta class for `ActionListSerializers` serializer."""
        model = models.DocsAction
        fields = (
            'id_action',
            'no_action',
            'action_type',
            'action_type_group',
            'description',
        )


class UsuarioSerializers(serializers.ModelSerializer):
    """Serializer to return the user who entered the `models.UsersCMR` data."""

    class Meta:
        """Meta class for `UsuarioSerializers` serializer."""
        model = models.UsersCMR
        fields = [
            'id_user',
            'first_name',
        ]


class DocsLandUserSerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocsLandUser` data.

    Data only for the action category linked to "USO_OCUPAÇÃO_DO_SOLO"
    """

    usercmr_id = UsuarioSerializers()
    action_id = ActionListSerializers()

    class Meta:
        """Meta class for `DocsLandUserSerializers` serializer."""
        model = models.DocsLandUser
        fields = [
            'nu_year',
            'nu_year_map',
        ] + list_fields_serializers_commun

    def to_representation(self, instance):
        """Method to return in `DocsLandUserSerializers` the full URL
        to download the documents in `models.DocsLandUser`.

        Returns:
            str: url to Land User document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(
            settings.DOCUMENTS_URL, instance.path_document)
        return url_document


class DocsDocumentTISerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocsDocumentTI` data.

    Data only for the action category linked to "DOCUMENTAL_TI".
    """

    usercmr_id = UsuarioSerializers()
    action_id = ActionListSerializers()

    class Meta:
        """Meta class for `DocsDocumentTISerializers` serializer."""
        model = models.DocsDocumentTI
        fields = [
            'dt_document',
            'no_extension',
        ] + list_fields_serializers_commun

    def to_representation(self, instance):
        """Method to return in `DocsDocumentTISerializers` the full URL to
        download the documents in `models.DocsDocumentTI`.

        Returns:
            str: url to DocumentTI document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(
            settings.DOCUMENTS_URL, instance.path_document)
        return url_document


class DocsMapotecaSerializers(serializers.ModelSerializer):
    """Serializer to return action category `models.DocsMapoteca` data.

    Data only for the action category linked to "MAPOTECA".
    """

    usercmr_id = UsuarioSerializers()
    action_id = ActionListSerializers()

    class Meta:
        """Meta class for `DocsMapotecaSerializers` serializer."""
        model = models.DocsMapoteca
        fields = [
            'no_description',
            'map_dimension',
            'js_ti',
        ] + list_fields_serializers_commun

    def to_representation(self, instance):
        """Method to return in `DocsMapotecaSerializers` the full URL to
        download the documents in `models.DocsMapoteca`.

        Returns:
            str: url to Mapoteca document
        """

        url_document = super().to_representation(instance)
        url_document['url_doc'] = urllib.parse.urljoin(
            settings.DOCUMENTS_URL, instance.path_document)
        return url_document


class DocsDocumentTIUploadSerializers(serializers.ModelSerializer):
    """Serializer for saving DOCUMENTS_TI `models.DocsMapoteca` data."""

    class Meta:
        """Meta class for `DocsDocumentTIUploadSerializers` serializer."""
        model = models.DocsDocumentTI
        fields = "__all__"

    def create(self, validated_data):
        """Method for saving  DocsDocumentTI serialized data on database.

        Args:
            validated_data (dict): DocsDocumentTI serialized data

        Returns:
            dict: DocsDocumentTI serialized data
        """
        result = models.DocsDocumentTI.objects.create(**validated_data)
        result.save()

        return result


class DocsLandUserUploadSerializers(serializers.ModelSerializer):
    """Serializer for saving DOCUMENTS_TI `models.DocsMapoteca` data."""

    class Meta:
        """Meta class for `DocsLandUserUploadSerializers` serializer."""
        model = models.DocsLandUser
        fields = "__all__"

    def create(self, validated_data):
        """Method for saving  DocsLandUser serialized data on database.

        Args:
            validated_data (dict): DocsLandUser serialized data

        Returns:
            dict: DocsLandUser serialized data
        """
        result = models.DocsLandUser.objects.create(**validated_data)
        result.save()

        return result


class DocsMapotecaUploadSerializers(serializers.ModelSerializer):
    """Serializer for saving DOCUMENTS_TI `models.DocsMapoteca` data."""

    class Meta:
        """Meta class for `DocsMapotecaUploadSerializers` serializer."""
        model = models.DocsMapoteca
        fields = "__all__"

    def create(self, validated_data):
        """Method for saving  DocsMapoteca serialized data on database.

        Args:
            validated_data (dict): DocsMapoteca serialized data

        Returns:
            dict: DocsMapoteca serialized data
        """
        result = models.DocsMapoteca.objects.create(**validated_data)
        result.save()

        return result
