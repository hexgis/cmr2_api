class FunaiRouter:
    """Router para a app funai."""

    route_app_labels = {'funai'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'db_for_read'
        return None

    def db_for_write(self, model, **hints):
        # Se realmente for só leitura
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return False
        return None
