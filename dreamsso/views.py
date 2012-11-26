
import django.contrib.auth.views
from django.conf import settings

def login(request, *args, **kwargs):
  if 'dreamsso.authbackend.saml.SamlBackend' in settings.AUTHENTICATION_BACKENDS \
          or 'dreamsso.authbackend.saml_local.SamlLocalBackend' in settings.AUTHENTICATION_BACKENDS:
    import djangosaml2.views
    return djangosaml2.views.login(request, *args, **kwargs)
  else:
    return django.contrib.auth.views.login(request, *args, **kwargs)

def logout(request, *args, **kwargs):
  if 'dreamsso.authbackend.saml.SamlBackend' in settings.AUTHENTICATION_BACKENDS \
          or 'dreamsso.authbackend.saml_local.SamlLocalBackend' in settings.AUTHENTICATION_BACKENDS:
    import djangosaml2.views
    return djangosaml2.views.logout(request, *args, **kwargs)
  else:
    return django.contrib.auth.views.logout(request, *args, **kwargs)

