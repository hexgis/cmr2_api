import logging
import ldap
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class MyLDAPBackend:
    """
    Custom authentication backend to authenticate FUNAI users via LDAP.

    FUNAI users can log in using only their username, but LDAP authentication
    is performed using the user's email. 
    This backend also falls back to Django's
    default authentication for non-FUNAI users.
    """

    def __init__(self):
        self.UserModel = get_user_model()

    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        """
        Authenticates a user using LDAP (for FUNAI users) or Django fallback.

        Args:
            request (HttpRequest): The incoming HTTP request.
            username_or_email (str): The username or email entered by the user.
            password (str): The provided password.
            **kwargs: Additional arguments.

        Returns:
            User | None: The authenticated user instance 
            or None if authentication fails.
        """
        if not username_or_email or not password:
            logger.debug("Username/email or password not provided.")
            return None

        user = self._get_user_by_username_or_email(username_or_email)

        if user and self._is_funai_user(user):
            if self._ldap_bind(user.email, password):
                logger.debug(
                    "LDAP bind successful for user: %s", user.username)
                if user.is_active:
                    return user
                logger.debug("User is not active: %s", user.username)
            else:
                logger.debug("LDAP bind failed for user: %s", user.username)
            return None

        if user and user.check_password(password):
            if user.is_active:
                logger.debug(
                    "User authenticated via Django: %s", user.username)
                return user
            logger.debug("User is not active: %s", user.username)

        return None

    def _get_user_by_username_or_email(self, identifier):
        """
        Retrieves a user by username or email.

        Args:
            identifier (str): The username or email.

        Returns:
            User | None: The user instance or None if not found.
        """
        try:
            return self.UserModel.objects.get(
                username=identifier
            ) if '@' not in identifier else self.UserModel.objects.get(
                email=identifier
            )

        except self.UserModel.DoesNotExist:
            logger.debug("User not found: %s", identifier)
            return None

    def _is_funai_user(self, user):
        """
        Checks if the user is a FUNAI user based on email domain.

        Args:
            user (User): The user instance.

        Returns:
            bool: True if the user is from FUNAI, False otherwise.
        """
        return user.email.endswith('@funai.gov.br')

    def _ldap_bind(self, email, password):
        """
        Attempts to authenticate (bind) with the LDAP server
        using email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the bind is successful, False otherwise.
        """
        connection = None
        try:
            connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            connection.set_option(ldap.OPT_REFERRALS, 0)
            connection.simple_bind_s(email, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            logger.debug("Invalid LDAP credentials for email: %s", email)
        except ldap.LDAPError as e:
            logger.error("LDAP error for email %s: %s", email, e)
        finally:
            if connection:
                try:
                    connection.unbind_s()
                except Exception:
                    pass
        return False

    def get_user(self, user_id):
        """
        Retrieves a user by their primary key.

        Args:
            user_id (int): The user's primary key.

        Returns:
            User | None: The user instance or None if not found.
        """
        try:
            return self.UserModel.objects.get(pk=user_id)
        except self.UserModel.DoesNotExist:
            return None
