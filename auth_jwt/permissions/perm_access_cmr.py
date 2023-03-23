from django.contrib.contenttypes.models import ContentType
from auth_jwt.permissions import permission_granted

# from rest_framework import (
#     generics,
#     # permissions,
#     )

# permi = ('catalog.view_satellite')
# permis = ('catalog.view_satellite', 'catalog.access_satellite')
# permis = ('catalog.add_satellite', 'catalog.access_satellite')
# CMR_Modulo_Access.user_request_permission(self.request.user)


class CMR_Modulo_Access():
    cmr_catalog_modulo = ("observar_satellite", "permissao_adicional_test")

    def app_name_exists(app_name):
        app_list = ContentType.objects.values_list(
            'app_label', flat=True).distinct()
        if app_name in str(app_list):
            return True
        else:
            return False

    def user_request_permission(request_user, app_name):
        if CMR_Modulo_Access.app_name_exists(app_name):
            # import pdb; pdb.set_trace()
            # print('messageDeu bom!!!\n\n', request_user, '!\n\n', app_name)
            # print("xpto ----->>>> ", request_user.has_perms(permission_granted.permissons_access[app_name]))
            return request_user.has_perms(permission_granted.permissons_access[app_name])
        else:
            print('messageDeu ruimmmm!!!\n\n', app_name)
