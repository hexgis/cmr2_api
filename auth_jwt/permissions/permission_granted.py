from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from auth_jwt.permissions import perm_access_cmr



permis_catalog_satellite = ('catalog.view_satellite',)
permis_catalog_catalogs = ('catalog.view_catalogs',)
# permi_access_catalog = ('catalog.view_satellite', 'catalog.access_satellite')#
permis_access_catalog = ('catalog.access_catalog', 'catalog.access_satellite')
permis_catalog = permis_catalog_satellite + permis_catalog_catalogs + permis_access_catalog
# CMR_Modulo_Access.user_request_permission(self.request.user)

permis_funai_limiteterraindigena = ('funai.view_limiteterraindigena',)
permis_funai_coordenacaoregional = ('funai.view_coordenacaoregional',)
permis_access_funai = ('funai.access_limiteterraindigena', 'funai.access_coordenacaoregional')
permis_funai = permis_funai_limiteterraindigena + permis_funai_coordenacaoregional + permis_access_funai

permissons_access = {
    'catalog':permis_access_catalog,
    'funai':permis_access_funai
}

###################################################################
# #Create permissions in app models: FUNAI and CATALOG
# #######
# from funai import models

# content_type = ContentType.objects.get_for_model(models.CoordenacaoRegional)
# permission = Permission.objects.create(codename="access_coordenacaoregional", name="Can access coordenacaoregional FUNAI in CMR", content_type=content_type)

# content_type = ContentType.objects.get_for_model(models.LimiteTerraIndigena)
# permission = Permission.objects.create(codename="access_limiteterraindigena", name="Can access limiteterraindigena FUNAI in CMR", content_type=content_type,)

# #######
# from catalog import models

# content_type = ContentType.objects.get_for_model(models.Catalogs)
# permission = Permission.objects.create(codename="access_catalogs", name="Can acesso catalogs CATALOG in CMR", content_type=content_type,)

# content_type = ContentType.objects.get_for_model(models.Satellite)
# permission = Permission.objects.create(codename="access_satellite", name="Can acesso satellite CATALOG in CMR", content_type=content_type,)
##################################################################
#grupos de permissões
groups = ['FUNAI_SEDE', 'FUANI_COORDENACAO_REGIONAL', 'FUNAI_TERRA_INDIGENA', 'FPE', 'OUTRAS_INSTITUICOES', 'ACADEMICO', 'CULTURAL', 'AUTENTICADO']
group_name = groups[6] #'CULTURAL'
list_users = ['Lucas', 'Sena', 'Test1', 'Test2']
#Criando grupos
[Group.objects.get_or_create(name=group) for group in groups]

#######
permissions = ['access_catalogs','access_satellite','view_satellite']
def add_permissions_in_group(group_name, permissions):
    """Função para adicionar os grupos"""
    group = Group.objects.get(name=group_name)
    permissions = Permission.objects.filter(codename__in=permissions)
    #remove as permissões
    group.permissions.clear()
    #Adiciona novas permissões
    for perm in permissions:
        group.permissions.add(perm)

#######
def create_new_users(list_users):
    """Criar Usuários"""
    for user in list_users:
        obj = User.objects.create_user(user)
        obj.set_password('123456')
        obj.save()

#######
def add_user_in_group(group_name, list_users):
    """Adiciona lista de usuários a um grupo."""
    group = Group.objects.get(name=group_name)
    for user in list_users:
        user_obj = User.objects.get(username = user)
        user_obj.groups.clear()
        user_obj.groups.add(group)