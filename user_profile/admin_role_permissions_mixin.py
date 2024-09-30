from django.core.exceptions import PermissionDenied

class AdminRolePermissionsMixin:
    admin_permission_checks = []

    def has_admin_permission(self, request):
        for check in self.admin_permission_checks:
            check(request)

    def changelist_view(self, request, extra_context=None):
        self.has_admin_permission(request)
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.has_admin_permission(request)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.has_admin_permission(request)
        return super().add_view(request, form_url, extra_context=extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        self.has_admin_permission(request)
        return super().delete_view(request, object_id, extra_context=extra_context)
