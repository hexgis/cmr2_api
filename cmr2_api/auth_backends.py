import ldap
import logging
from django_auth_ldap.backend import LDAPBackend

logger = logging.getLogger('auth_backends')

class MyLDAPBackend(LDAPBackend):
    def authenticate_ldap_user(self, ldap_user, password):
        logger.debug(f"Trying to authenticate user {ldap_user.dn} with password {password}")
        logger.debug(f"Connecting to LDAP server {self.settings.SERVER_URI}")

        try:
            user = super().authenticate_ldap_user(ldap_user, password)
            if user:
                logger.debug(f"Authenticated user {user.username} successfully")
            else:
                logger.debug("Failed to authenticate user")
            return user
        except ldap.LDAPError as e:
            logger.error(f"LDAP error: {e}")
            return None