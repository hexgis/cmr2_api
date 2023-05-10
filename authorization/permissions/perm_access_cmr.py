from django.apps import apps

from django.contrib.auth.models import Permission


class CMRModuleAccess():
    """Management of the first level of access to the CMR Modules."""
    def cmr_permissions_access(app_name):
        """Concatenates the action access with the name of the app to assemble
        the CMR Modules access permission."""
        app_access_permissions=()
        codenames=Permission.objects.values_list("codename",flat=True).filter(
            codename__icontains="access", 
            content_type_id__app_label__exact=app_name)

        for coodename in codenames:
            app_access_permissions += (app_name + "." + coodename,)

        return app_access_permissions

    def user_request_permission(request_user, app_name):
        """Checks if the logged in user has the necessary permission to access
        the CMR Modules in app_name."""
        if apps.get_app_config(app_name):
            app_access_permissions = CMRModuleAccess.cmr_permissions_access(
                app_name)
            if len(app_access_permissions) <= 1:
                cmr_permission = request_user.has_perm(app_access_permissions)
            else:
                cmr_permission = request_user.has_perms(app_access_permissions)
            return cmr_permission
