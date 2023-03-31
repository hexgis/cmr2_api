from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


class CMRModuloAccess():
    """Management of the first level of access to the CMR Modules."""
    def app_name_exists(app_name):
        """Checks if the passed APP name exists in the project.

        Reurns:
            True: APP exist or
            False: APP no exist
        """
        app_list = ContentType.objects.values_list(
            'app_label', flat=True).distinct()
        
        if app_name in str(app_list):
            return True
        else: #TODO: Add execeptions
            return False

    def cmr_permissions_access(app_name):
        """Concatenates the action access with the name of the app to assemble
        the CMR Modules access permission."""
        app_access_permissions=()
        codenames = Permission.objects.values_list("codename",flat=True).filter(
            codename__icontains="access", 
            content_type_id__app_label__exact=app_name)

        for coodename in codenames:
            app_access_permissions += (app_name + "." + coodename,)

        return app_access_permissions

    def user_request_permission(request_user, app_name):
        """checks if the logged in user has the necessary permission to access
        the CMR Modules."""
        if CMRModuloAccess.app_name_exists(app_name):
            app_access_permissions = CMRModuloAccess.cmr_permissions_access(app_name)
            if len(app_access_permissions) <= 1:
                cmr_permission = request_user.has_perm(app_access_permissions)
            else:
                cmr_permission = request_user.has_perms(app_access_permissions)
            return cmr_permission
        else:
            return False
