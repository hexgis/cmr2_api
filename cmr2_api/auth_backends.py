import logging
import ldap
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django_auth_ldap.backend import LDAPBackend

logger = logging.getLogger(__name__)


class MyLDAPBackend(LDAPBackend):
    """
    Custom LDAP backend that attempts to authenticate the user against an LDAP server.
    If authentication is successful, it returns the Django user object
    associated with the email. Otherwise, returns None.
    """

    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        """
        Authenticates the user with LDAP
        using the provided username_or_email and password.
        If successful, returns the Django user with the same email,
        or None otherwise.
        """

        UserModel = get_user_model()

        if not username_or_email or not password:
            logger.debug("username_or_email or password is empty.")
            return None

        # 1. Try to authenticate with LDAP
        # (only for users who have a funai email address)
        if '@funai.gov.br' in username_or_email:
            if not self._ldap_bind(username_or_email, password):
                logger.debug(
                    "LDAP bind failed for email: %s",
                    username_or_email
                )
                return None

            logger.debug(
                "LDAP bind successful for email: %s",
                username_or_email
            )

            user = UserModel.objects.get(email=username_or_email)
            return user

        # 2. Check if there is a user in Django
        user = self._get_django_user(username_or_email)
        if user:
            logger.debug(
                "User found in Django database via email: %s",
                username_or_email
            )
        else:
            logger.debug(
                "User not found in Django database via email: %s",
                username_or_email
            )
        return user

    def _ldap_bind(self, dn, password):
        """
        Attempts to authenticate to the LDAP server with the credentials.
        Returns True if successful, False otherwise.
        """
        try:
            connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            connection.set_option(ldap.OPT_REFERRALS, 0)
            connection.simple_bind_s(dn, password)
            connection.unbind_s()
            return True
        except ldap.INVALID_CREDENTIALS:
            logger.debug(
                "Invalid credentials for DN: %s",
                dn
            )
        except ldap.LDAPError as e:
            logger.error(
                "LDAP error occurred during bind for DN %s: %s",
                dn,
                e
            )
        finally:
            # If unsuccessful, try unbind to free up resources
            try:
                connection.unbind_s()
            except Exception:
                pass

        return False

    def _get_django_user(self, username_or_email):
        """
        Attempts to search for the user by email or username,
        depending on the format provided.
        """
        UserModel = get_user_model()

        try:
            if '@' in username_or_email:
                user = UserModel.objects.get(email=username_or_email)
            else:
                user = UserModel.objects.get(username=username_or_email)
            return user
        except UserModel.DoesNotExist:
            return None
