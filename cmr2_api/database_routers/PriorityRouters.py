"""Database routers."""


class PriorityRouter:
    """Priority database router."""

    route_app_labels = {'priority_monitoring'}

    def db_for_read(self, model, **hints):
        """Database for read method."""
        if model._meta.app_label in self.route_app_labels:
            return 'priority_database'
        return None

    def db_for_write(self, model, **hints):
        """Database for write."""
        return False

    def allow_relation(self, obj1, obj2, **hints):
        """Relationing database."""
        if obj1._meta.app_label in self.route_app_labels or \
           obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow database migration."""
        if app_label in self.route_app_labels:
            return db == 'priority_database'
        return None