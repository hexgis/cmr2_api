import logging
import ldap
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class MyLDAPBackend:
    """
    Custom LDAP backend that authenticates users against an LDAP server (AD)
    for @funai.gov.br emails and returns the Django user object.
    """

    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        UserModel = get_user_model()

        if not username_or_email or not password:
            logger.debug("username_or_email or password is empty.")
            return None

        # Autenticação via LDAP para usuários @funai.gov.br
        if '@funai.gov.br' in username_or_email:
            if not self._ldap_bind(username_or_email, password):
                logger.debug("LDAP bind failed for email: %s",
                             username_or_email)
                return None

            logger.debug("LDAP bind successful for email: %s",
                         username_or_email)

            try:
                user = UserModel.objects.get(email=username_or_email)
                logger.debug(
                    f"User found: {user.username} (email: {user.email})")
                return user
            except UserModel.DoesNotExist:
                logger.debug(
                    "User %s not found in Django database.", username_or_email)
                # Opcional: Criar usuário se não existir
                user = UserModel.objects.create_user(
                    username=username_or_email.split(
                        '@')[0],  # Ajuste conforme necessário
                    email=username_or_email,
                    password=None  # Senha vazia, já que é autenticado via AD
                )
                user.is_active = True
                user.save()
                logger.debug(
                    f"User created: {user.username} (email: {user.email})")
                return user

        # Fallback para autenticação padrão do Django (se necessário)
        try:
            user = UserModel.objects.get(username=username_or_email)
            if user.check_password(password):
                logger.debug("User authenticated via Django: %s",
                             username_or_email)
                return user
        except UserModel.DoesNotExist:
            logger.debug("User %s not found in Django database.",
                         username_or_email)

        return None

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
            logger.debug("Invalid credentials for DN: %s", dn)
        except ldap.LDAPError as e:
            logger.error(
                "LDAP error occurred during bind for DN %s: %s", dn, e)
        finally:
            try:
                connection.unbind_s()
            except Exception:
                pass
        return False

    def get_user(self, user_id):
        """
        Required method to retrieve a user by ID.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
