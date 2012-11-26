
"""
Django authentication backend for SAML2
This differs from SamlBackend by using direct access to userdb database,
when SamlBackend uses http-api. This means that dream-userdb must be installed
as app in the project.

Register the backends::

  AUTHENTICATION_BACKENDS = (
    'dreamsso.authbackend.saml_local.SamlLocalBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

You can also enable normal if you want to allow local logins
for e.g. admin users.

Add SAML URLs to urlconf::

  import djangosaml2.urls
  urlpatterns += patterns('', (r'^saml/', include(djangosaml2.urls)))

Install package djangosaml2 and all of its dependencies.

"""
import logging
from django.contrib.auth.backends import ModelBackend
from dreamsso.models import User
try:
    import dreamuserdb
except ImportError as e:
    raise ImportError('dreamuserdb is required with this backend. Exception was: %s' % str(e))

LOG = logging.getLogger(__name__)

def _get(saml, name, default=None):
  if name in saml:
    try:
      return saml[name][0]
    except IndexError:
      return default
  return default

class SamlLocalBackend(ModelBackend):
  supports_anonymous_user = True
  supports_inactive_user = True
  supports_object_permissions = False

  def authenticate(self, session_info=None, attribute_mapping=None, create_unknown_user=True):
    if not session_info and 'ava' in session_info:
      return None
    saml = session_info['ava']
    LOG.debug('SAML login', extra={'data': saml})
    user = User.objects.get(id=_get(saml, 'id', None))
    user.update_permissions_from_roles()
    LOG.debug('Logged in as %s' % user)
    return user

  def get_user(self, user_id):
    user = User.objects.get(id=user_id)
    user.update_permissions_from_roles()
    return user


  #def has_perm(self, user, perm, obj=None):

  #def has_module_perms(self, user, app_label, obj=None):

  #def get_group_permissions(self, user, obj=None):

  #def get_all_permissions(self, user, obj=None):

