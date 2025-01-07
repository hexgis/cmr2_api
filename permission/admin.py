from django import forms
from django.contrib.gis import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.conf import settings

from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ImportExportActionModelAdmin as import_export

from layer import models as layer_models
from user import models as user
from permission import models


class PermissionAdminForm(forms.ModelForm):
    """Form used in the admin interface for managing Groups.

    Forces the multiple choice fields refresh as the data is being updated.
    """

    groups = forms.ModelMultipleChoiceField(
        queryset=user.Group.objects.all(),
        widget=FilteredSelectMultiple(('Groups'), False),
        required=False
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form with optional initial values."""

        super(PermissionAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['groups'].initial = \
                self.instance.groups.all()

    def save(self, commit=True):
        """Save the form data to the database.

        Args:
            commit (bool, optional): Indicates whether to save the instance
            to the database immediately. Defaults to True.

        Returns:
            Group: The saved or updated Group instance.
        """

        groups = super(PermissionAdminForm, self).save(commit=False)

        if commit:
            groups.save()

        if groups.pk:
            groups.groups.set(self.cleaned_data['groups'])
            self.save_m2m()

        return groups


class LayerPermissionAdminForm(PermissionAdminForm):
    """Admin form for managing permissions related to layers."""

    layers = forms.ModelMultipleChoiceField(
        queryset=layer_models.Layer.objects.all(),
        widget=FilteredSelectMultiple('Layers', False),
        required=False,
    )


class LayerPermissionAdmin(LeafletGeoAdmin, import_export):
    """Admin class for LayerPermission model data."""

    form = LayerPermissionAdminForm

    list_display = (
        'name',
        'description',
    )

    fieldsets = (
        (None, {'fields': (
            'name',
            'description',
            'layers',
        )}),
        ('Groups', {'fields': (
            'groups',
        )}),
    )

    search_fields = list_display

    filter_fields = list_display


class ComponentPermissionAdminForm(PermissionAdminForm):
    """Admin form for managing permissions related to components."""

    components = forms.MultipleChoiceField(
        choices=settings.COMPONENT_LIST,
        widget=FilteredSelectMultiple("Opções", is_stacked=False)
    )

    class Meta:
        """Meta class for ComponentPermissionAdminForm."""

        model = models.ComponentPermission
        fields = '__all__'

    def clean_components(self):
        """Clean the components field."""

        data = self.cleaned_data['components']
        return data


class ComponentPermissionAdmin(LeafletGeoAdmin, import_export):
    """Admin class for ComponentPermission model data."""

    form = ComponentPermissionAdminForm

    list_display = (
        'name',
        'description',
    )

    fieldsets = (
        (None, {'fields': (
            'name',
            'description',
            'components',
        )}),
        ('Groups', {'fields': (
            'groups',
        )}),
    )

    search_fields = list_display

    filter_fields = list_display


admin.site.register(models.LayerPermission, LayerPermissionAdmin)
admin.site.register(models.ComponentPermission, ComponentPermissionAdmin)
