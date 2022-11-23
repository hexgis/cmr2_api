"""Database routers catalog app."""


class CatalogRouter:
    """Catalog tables, database router."""

    route_app_labels = {'catalog'}
    model_catalog = 'Catalog'

    def db_for_read(self, model, **hints):
        """Database for read method."""
        if model._meta.app_label in self.route_app_labels:
            # return 'db_for_read'
            
            # import pdb; pdb.set_trace()
            if model._meta.model_name == self.model_catalog.lower():
                # import pdb; pdb.set_trace()
                print('------------>>>>>>>>>------------------------------------- \n\n\n')
                print("Model = ", model._meta.model_name == self.model_catalog.lower())
                print('------------>>>>>>>>>------------------------------------- \n\n\n')
                return 'db_for_read'
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
            return db == 'db_for_read'
        return None

# class AccountsDBRouter:
#        def db_for_read (self, model, **hints):
#           if (model == Accounts):
#              # your model name as in settings.py/DATABASES
#              return 'accounts'
#           return None
       
#        def db_for_write (self, model, **hints):
#           if (model == Accounts):
#              # your model name as in settings.py/DATABASES
#              return 'accounts'
#           return None