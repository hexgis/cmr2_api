from rolepermissions.permissions import get_user_roles

class AdminPermissionMixin:
    """
        Mixin class to handle permission checks based on user roles and group membership.
    """
    allowed_roles = []

    def has_master_admin_role(self, user):
        """
            Checks if the user has the 'dev_master_admin' role or is in the 'dev_master_admin' group.

            Args:
            - user: The user object to check.

            Returns:
            - bool: True if the user has the 'dev_master_admin' role or group, False otherwise.
        """
        user_roles = get_user_roles(user)
        return any(role.get_name() == 'dev_master_admin' for role in user_roles) or user.groups.filter(name='dev_master_admin').exists()
    
    def has_add_permission(self, request):
        """
            Checks if the user has permission to add objects. Only users with the 'dev_master_admin' role or group are allowed.

            Args:
            - request: The HTTP request object.

            Returns:
            - bool: True if the user has the 'dev_master_admin' role or group, False otherwise.
        """
        return self.has_master_admin_role(request.user)
    
    def has_view_permission(self, request, obj=None):
        """
            Checks if the user has permission to view objects. Only users with the 'dev_master_admin' role or group are allowed.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has the 'dev_master_admin' role or group, False otherwise.
        """
        return self.has_master_admin_role(request.user)
    
    def has_change_permission(self, request, obj=None):
        """
            Checks if the user has permission to change objects. Only users with the 'dev_master_admin' role or group are allowed.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: True if the user has the 'dev_master_admin' role or group, False otherwise.
        """
        return self.has_master_admin_role(request.user)
    
    def has_delete_permission(self, request, obj=None):
        """
            Checks if the user has permission to delete objects. Deletion is always disallowed.

            Args:
            - request: The HTTP request object.
            - obj: The object being accessed (default is None).

            Returns:
            - bool: False, deletion is always disallowed.
        """
        return self.has_master_admin_role(request.user)