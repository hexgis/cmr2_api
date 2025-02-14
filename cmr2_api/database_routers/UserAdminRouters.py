class UserAdminRouter:
    """Router apps for admin and user."""

    route_app_labels = {'user', 'admin_panel', 'admin', 'dashboard'}

    def db_for_write(self, model, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'default'
        return None
