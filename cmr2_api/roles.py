from rolepermissions.roles import AbstractUserRole
from cmr2_api import permissions

class FunaiSede(AbstractUserRole):
    """Role for users in the Funai Sede group."""
    available_permissions = permissions.common_user_permissions

class FunaiCoordenacaoRegional(AbstractUserRole):
    """Role for users in the Funai Coordenacao Regional group."""
    available_permissions = permissions.common_user_permissions

class FunaiTerraIndigena(AbstractUserRole):
    """Role for users in the Funai Terra Indigena group."""
    available_permissions = permissions.common_user_permissions

class Fpe(AbstractUserRole):
    """Role for users in the Fpe group."""
    available_permissions = permissions.common_user_permissions

class OutrasInstituicoes(AbstractUserRole):
    """Role for users in the Outras Instituicoes group."""
    available_permissions = permissions.common_user_permissions

class Academico(AbstractUserRole):
    """Role for users in the Academico group."""
    available_permissions = permissions.common_user_permissions

class Cultural(AbstractUserRole):
    """Role for users in the Cultural group."""
    available_permissions = permissions.common_user_permissions

class Autenticado(AbstractUserRole):
    """Role for authenticated users."""
    available_permissions = permissions.common_user_permissions

class NaoAutenticado(AbstractUserRole):
    """Role for non-authenticated users."""
    available_permissions = permissions.default_user_permissions

class FunaiCmrAdmin(AbstractUserRole):
    """Role for Funai CMR administrators."""
    available_permissions = permissions.all_funai_panel_permissions

class DevMasterAdmin(AbstractUserRole):
    """Role for developers with master admin privileges."""
    available_permissions = permissions.all_dev_mater_permissions
