import ldap
import logging
from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth.models import User
from django.conf import settings

logger = logging.getLogger('auth_backends')

class MyLDAPBackend(LDAPBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            logger.debug("Username or password is empty.")
            return None

        # Usar o email diretamente
        email = username
        user_dn = email  # Usar o email diretamente como DN

        try:
            # Conectar ao servidor LDAP com as credenciais fornecidas pelo usuário
            ldap_connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
            ldap_connection.simple_bind_s(user_dn, password)
            ldap_connection.unbind()
            
            logger.debug("LDAP bind successful for email: %s", email)
            
            # Autenticação bem-sucedida no LDAP, buscar o usuário no Django
            try:
                # Buscar usuário no Django por email
                user = User.objects.get(email=email)
                logger.debug("User found in Django database: %s", email)
            except User.DoesNotExist:
                logger.debug("User not found in Django database: %s", email)
                user = None

            return user
        except ldap.INVALID_CREDENTIALS:
            # Verificar se o usuário existe no LDAP antes de logar a senha incorreta
            ldap_connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
            
            try:
                # Tentativa de bind com uma senha inválida para verificar se o usuário existe
                ldap_connection.simple_bind_s(user_dn, 'wrongpassword')
                ldap_connection.unbind()
            except ldap.INVALID_CREDENTIALS:
                # O usuário não existe ou a senha está incorreta
                logger.debug("Invalid credentials provided for email: %s. The password may be incorrect.", email)
            except ldap.LDAPError as e:
                logger.error("LDAP error occurred while verifying user existence: %s", e)
            finally:
                ldap_connection.unbind()

            return None
        except ldap.LDAPError as e:
            logger.error("LDAP error occurred: %s", e)
            return None
