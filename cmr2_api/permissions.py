from rolepermissions.roles import AbstractUserRole

##########################
### Module Permissions ###
##########################

# Default permissions for a generic user
default_user_permissions = {
    'visualizar_home': True,  # Permission to view the home page
}

# Permissions for managing users in the admin panel
admin_user_panel_permissions = {
    'visualizar_painel_de_usuarios': True,  # Permission to view the user panel
    'adicionar_usuario': True,              # Permission to add users
    'alterar_usuario': True,                # Permission to change user details
    'alterar_status_do_usuario': True,      # Permission to change user status
    'alterar_grupo_do_usuario': True,       # Permission to change user group
    'alterar_permissoes_do_usuario': True,  # Permission to change user permissions

    'visualizar_painel_grupos': True, # Permission to view the groups panel
    'adicionar_grupo': True, # Permission to change one group
    'alterar_grupo': True, # Permission to create a new group
}

# Permissions for support-related actions
support_permissions = {
    'visualizar_support': True,  # Permission to view support
    'adicionar_support': True,   # Permission to add support items
    'alterar_support': True,     # Permission to change support items

    'vizualizar_support_geoserver': True,
    'adicionar_support_geoserver': True,
    'alterar_support_geoserver': True,

    'vizualizar_support_camadas': True,
    'adicionar_support_camadas': True,
    'alterar_support_camadas': True,

    'vizualizar_': True,
    'adicionar_': True,
    'alterar_': True,
}

# Permissions related to FUNAI functionalities
funai_permissions = {
    'visualizar_funai_coordenacao_reginal': True,  # Permission to view FUNAI regional coordination
    'adicionar_funai_coordenacao_reginal': True,   # Permission to add FUNAI regional coordination
    'alterar_funai_coordenacao_reginal': True,     # Permission to change FUNAI regional coordination

    'visualizar_funai_terras_indigenas': True,     # Permission to view indigenous lands
    'adicionar_funai_terras_indigenas': True,      # Permission to add indigenous lands
    'alterar_funai_terras_indigenas': True,        # Permission to change indigenous lands

    'visualizar_funai_instrumento_gestao': True,   # Permission to view management instruments
    'adicionar_funai_instrumento_gestao': True,    # Permission to add management instruments
    'alterar_funai_instrumento_gestao': True,      # Permission to change management instruments
}

# Permissions related to documental functionalities
documental_permissions = {
    'visualizar_documental_acoes': True,           # Permission to view documental actions
    'adicionar_documental_acoes': True,            # Permission to add documental actions
    'alterar_documental_acoes': True,              # Permission to change documental actions
    'visualizar_documental_terras_indigenas': True,  # Permission to view indigenous lands documentation
    'adicionar_documental_terras_indigenas': True,   # Permission to add indigenous lands documentation
    'alterar_documental_terras_indigenas': True,     # Permission to change indigenous lands documentation
    'visualizar_documental_terras_usuario': True,    # Permission to view user lands documentation
    'adicionar_documental_terras_usuario': True,     # Permission to add user lands documentation
    'alterar_documental_terras_usuario': True,       # Permission to change user lands documentation
    'visualizar_documental_mapoteca': True,          # Permission to view mapoteca
    'adicionar_documental_mapoteca': True,           # Permission to add mapoteca items
    'alterar_documental_mapoteca': True,             # Permission to change mapoteca items
    'visualizar_documental_usuarios_cmr': True,      # Permission to view CMR users documentation
    'adicionar_documental_usuarios_cmr': True,       # Permission to add CMR users documentation
    'alterar_documental_usuarios_cmr': True,         # Permission to change CMR users documentation
}

# Permissions related to the catalog functionalities
catalog_permissions = {
    'visualizar_catalog': True,  # Permission to view catalog
    'adicionar_catalog': True,   # Permission to add catalog items
    'alterar_catalog': True,     # Permission to change catalog items
}

camadas_sob_permissions = {
    '319': True,
    '1': True,
    '3': True,
    '6': True,
    '4': True,
    '5': True,
    '7': True,
}

##############################
### Dev Master Permissions ###
##############################

# Combine all permissions for the 'dev_master_admin' role
all_dev_mater_permissions = {}
all_dev_mater_permissions.update(default_user_permissions)
all_dev_mater_permissions.update(admin_user_panel_permissions)
all_dev_mater_permissions.update(support_permissions)
all_dev_mater_permissions.update(funai_permissions)
all_dev_mater_permissions.update(catalog_permissions)
all_dev_mater_permissions.update(documental_permissions)

# Set all combined permissions to True for 'dev_master_admin'
for permission in all_dev_mater_permissions:
    all_dev_mater_permissions[permission] = True

#####################################
### Admin Funai Panel Permissions ###
#####################################

# Combine all permissions for the 'funai_admin' role
all_funai_panel_permissions = {}
all_funai_panel_permissions.update(default_user_permissions)
all_funai_panel_permissions.update(admin_user_panel_permissions)
all_funai_panel_permissions.update(support_permissions)
all_funai_panel_permissions.update(funai_permissions)
all_funai_panel_permissions.update(catalog_permissions)
all_funai_panel_permissions.update(documental_permissions)

# Set all combined permissions to True for 'funai_admin'
for permission in all_funai_panel_permissions:
    all_funai_panel_permissions[permission] = True

#####################################
###    Common User Permissions    ###
#####################################

# Combine common permissions for general users
common_user_permissions = {}
common_user_permissions.update(camadas_sob_permissions)
