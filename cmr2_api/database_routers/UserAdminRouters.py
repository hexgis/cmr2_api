"""Database routers for the user and admin apps."""


class UserAdminRouter:
    """Router for the user and admin apps."""

    route_app_labels = {'user', 'admin'}
    model_user = 'User'  # Nome do modelo principal do app user
    model_admin = 'LogEntry'  # Modelo principal do admin (padrão do Django)

    def db_for_read(self, model, **hints):
        """Database for read operations."""
        if model._meta.app_label in self.route_app_labels:
            try:
                if model._meta.model_name in {self.model_user.lower(), self.model_admin.lower()}:
                    return 'db_for_read'
                else:
                    return 'default'
            except NameError:
                print(
                    "Warning: Exception in UserAdminRouter.db_for_read - ",
                    model._meta.app_label
                )
        return None

    def db_for_write(self, model, **hints):
        """Database for write operations."""
        try:
            if model._meta.model_name in {self.model_user.lower(), self.model_admin.lower()}:
                return False  # Impede escritas no db_for_read
            else:
                return 'default'
        except NameError:
            print(
                "Warning: Exception in UserAdminRouter.db_for_write - ",
                model._meta.app_label
            )

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations between models."""
        if obj1._meta.app_label in self.route_app_labels or \
           obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Control migration permissions."""
        if app_label in self.route_app_labels:
            try:
                if model_name in {self.model_user.lower(), self.model_admin.lower()}:
                    return db == 'db_for_read'  # Bloqueia migrações no db_for_read
                else:
                    return db == 'default'  # Aplica no default
            except NameError:
                print(
                    "Warning: Exception in UserAdminRouter.allow_migrate - ",
                    app_label
                )
        return None
