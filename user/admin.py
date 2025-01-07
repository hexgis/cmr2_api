import base64
from django import forms
from django.utils.html import format_html
from django.db import models as django_models
from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from leaflet.admin import LeafletGeoAdmin
from django_json_widget.widgets import JSONEditorWidget
from import_export.admin import ImportExportActionModelAdmin as import_export

from permission import models as permission_models
from user import models


class UploadedFileAdmin(import_export):
    """Admin class for UserUploadedFile model data."""

    list_display = (
        'name',
        'user',
        'date_created',
        'is_active',
    )

    search_fields = (
        'name',
        'user',
    )

    filter_fields = (
        'user_uploaded',
        'date_created',
    )

    readonly_fields = (
        'date_created',
    )


class UploadedFileGeometriesAdmin(LeafletGeoAdmin):
    """Admin class for UserUploadedFileGeometry model data."""

    formfield_overrides = {
        django_models.JSONField: {'widget': JSONEditorWidget},
    }

    def get_queryset(self, request):
        """Get Queryset for `models.UserUploadedFileGeometriesAdmin`.

        Args:
            request (request): default request.

        Returns:
            Queryset: filtered queryset
        """

        queryset = super(
            UploadedFileGeometriesAdmin, self
        ).get_queryset(request)

        return queryset.filter(user_uploaded__is_active=True)

    list_display = (
        'id',
        'user_uploaded',
        'properties',
    )

    search_fields = (
        'user_uploaded',
        'name',
    )

    filter_fields = (
        'user_uploaded',
    )


class UserAdminForm(forms.ModelForm):
    """Form used in the admin interface for managing Users.

    Forces the multiple choice fields refresh as the data is being updated.
    """

    roles = forms.ModelMultipleChoiceField(
        queryset=models.Role.objects.all(),
        widget=FilteredSelectMultiple('Roles', False),
        required=False
    )

    password = ReadOnlyPasswordHashField(
        label=('Password'),
        help_text=(
            'Raw passwords are not stored, so there is no way to see this \
            user’s password, but you can change the password using <a \
            href=\"../password/\">this form</a>.'
        )
    )


class CustomUserAdmin(UserAdmin, LeafletGeoAdmin, import_export):
    """Admin class for User model data."""

    def avatar(self, instance: models.User) -> str:
        """Get thumbnail image in html format.

        Args:
            instance (models.Vector): Vector model data.

        Returns:
            models.Vector: string info.
        """

        if instance.avatar_blob:
            img = base64.b64encode(instance.avatar_blob).decode('UTF-8')
            return format_html(
                f'<img src=data:image/png;base64,{img} height=40>'
            )
        else:
            return None

    form = UserAdminForm

    fieldsets = (
        (None, {'fields': (
            'email',
            'username',
            'password',
            'institution'
        )}),
        ('Personal info', {
         'fields': (
             'first_name',
             'last_name',
         )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'roles',
            'user_permissions'
        )}),
        ('Preferences', {'fields': (
            'avatar',
            'token',
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'institution'
            )
        }),
    )

    list_display = (
        'username',
        'first_name',
        'last_name',
    )

    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )

    ordering = ('username',)

    filter_horizontal = ('groups', 'user_permissions',)


class GroupAdminForm(forms.ModelForm):
    """Form used in the admin interface for managing Groups.

    Forces the multiple choice fields refresh as the data is being updated.
    """

    layer_permissions = forms.ModelMultipleChoiceField(
        queryset=permission_models.LayerPermission.objects.all(),
        widget=FilteredSelectMultiple('Layer permissions', False),
        required=False
    )

    component_permissions = forms.ModelMultipleChoiceField(
        queryset=permission_models.ComponentPermission.objects.all(),
        widget=FilteredSelectMultiple('Component permissions', False),
        required=False
    )

    roles = forms.ModelMultipleChoiceField(
        queryset=models.Role.objects.all(),
        widget=FilteredSelectMultiple(('Roles'), False),
        required=False
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form with optional initial values."""

        super(GroupAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['roles'].initial = \
                self.instance.roles.all()

    def save(self, commit=True):
        """Save the form data to the database.

        Args:
            commit (bool, optional): Indicates whether to save the instance
            to the database immediately. Defaults to True.

        Returns:
            Role: The saved or updated Role instance.
        """

        roles = super(GroupAdminForm, self).save(commit=False)

        if commit:
            roles.save()

        if roles.pk:
            roles.roles.set(self.cleaned_data['roles'])
            self.save_m2m()

        return roles


class InstitutionAdmin(import_export):
    """Admin class for Institution model data."""

    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )


class GroupAdmin(import_export):
    """Admin class for Group model data."""

    form = GroupAdminForm

    fieldsets = (
        (None, {'fields': (
            'name',
            'description'
        )}),
        ('Permissions', {'fields': (
            'layer_permissions',
            'component_permissions'
        )}),
        ('Roles', {'fields': (
            'roles',
        )}),
    )


class RoleAdminForm(forms.ModelForm):
    """Form used in the admin interface for managing Roles.

    Forces the multiple choice fields refresh as the data is being updated.
    """

    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.all(),
        widget=FilteredSelectMultiple('Groups', False),
        required=False
    )

    users = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.all(),
        widget=FilteredSelectMultiple(('Users'), False),
        required=False
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form with optional initial values."""

        super(RoleAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['users'].initial = \
                self.instance.users.all()

    def save(self, commit=True):
        """Save the form data to the database.

        Args:
            commit (bool, optional): Indicates whether to save the instance
            to the database immediately. Defaults to True.

        Returns:
            User: The saved or updated User instance.
        """

        users = super(RoleAdminForm, self).save(commit=False)

        if commit:
            users.save()

        if users.pk:
            users.users.set(self.cleaned_data['users'])
            self.save_m2m()

        return users


class RoleAdmin(import_export):
    """Admin class for Role model data."""

    form = RoleAdminForm

    fieldsets = (
        (None, {'fields': (
            'name',
            'description'
        )}),
        ('Groups', {'fields': (
            'groups',
        )}),
        ('Users', {'fields': (
            'users',
        )}),
    )


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Institution, InstitutionAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.UserUploadedFile, UploadedFileAdmin)
admin.site.register(models.UserUploadedFileGeometry,
                    UploadedFileGeometriesAdmin)
