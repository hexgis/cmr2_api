"""Database routers catalog app."""


class FunaiRouter:
    """Catalog tables, database router."""

    route_app_labels = {'funai'}
    model_funai = 'LimiteTerraIndigena'

    def db_for_read(self, model, **hints):
        """Database for read method."""
        if model._meta.app_label in self.route_app_labels:
            try:
                if model._meta.model_name == self.model_funai.lower():
                    return 'db_for_read'
                else:
                    return 'default'
            except NameError:
                print(
                    "warning: Call the exception in FunaiRouter. db_for_read: ",
                    model._meta.app_label
                )
        return None

    def db_for_write(self, model, **hints):
        """Database for write."""
        try:
            if model._meta.model_name == self.model_funai.lower():
                return False
            else:
                return 'default'
        except NameError:
            print(
                "warning: Call the exception in FunaiRouter.db_for_write: ",
                model._meta.app_label
            )

    def allow_relation(self, obj1, obj2, **hints):
        """Relationing database."""
        if obj1._meta.app_label in self.route_app_labels or \
           obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow database migration."""
        # TODO: Investigate this function to identify a way to avoid falling \
        # into the EXECEPT.
        if app_label in self.route_app_labels:
            try:
                if model._meta.model_name == self.model_funai.lower():
                    return db == 'db_for_read'
                else:
                    return db == 'default'
            except NameError:
                print(
                    "warning: Call the exception in FunaiRouter. allow_migrate: ",
                      app_label
                )
        return None
