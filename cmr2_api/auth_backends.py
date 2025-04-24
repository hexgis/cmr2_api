import logging
import ldap
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class MyLDAPBackend:
    """
    Custom LDAP backend that authenticates users against an LDAP server (AD)
    for @funai.gov.br emails and returns the Django user object.
    """

    def __init__(self):
        self.UserModel = get_user_model()

    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        if not username_or_email or not password:
            logger.debug("Username or password is missing.")
            return None

        if self._is_funai_email(username_or_email):
            return self._authenticate_via_ldap(username_or_email, password)

        return self._authenticate_via_django(username_or_email, password)

    def _is_funai_email(self, email):
        return email.endswith('@funai.gov.br')

    def _authenticate_via_ldap(self, email, password):
        try:
            user = self.UserModel.objects.get(email=email)
        except self.UserModel.DoesNotExist:
            logger.debug("LDAP user not found in local DB: %s", email)
            return None

        if not self._ldap_bind(email, password):
            logger.debug("LDAP bind failed for: %s", email)
            return None

        if user.is_active:
            logger.debug("LDAP authentication successful for: %s", email)
            return user

        logger.debug("LDAP user is not active: %s", email)
        return None

    def _authenticate_via_django(self, username, password):
        try:
            user = self.UserModel.objects.get(username=username)
        except self.UserModel.DoesNotExist:
            logger.debug("Django user not found: %s", username)
            return None

        if user.check_password(password):
            if user.is_active:
                logger.debug(
                    "Django authentication successful for: %s", username)
                return user
            logger.debug("Django user is not active: %s", username)

        return None

    def _ldap_bind(self, dn, password):
        connection = None
        try:
            connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            connection.set_option(ldap.OPT_REFERRALS, 0)
            connection.simple_bind_s(dn, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            logger.debug("Invalid LDAP credentials for: %s", dn)
        except ldap.LDAPError as e:
            logger.error("LDAP error for %s: %s", dn, e)
        finally:
            if connection:
                try:
                    connection.unbind_s()
                except Exception:
                    pass
        return False

    def get_user(self, user_id):
        try:
            return self.UserModel.objects.get(pk=user_id)
        except self.UserModel.DoesNotExist:
            return None
