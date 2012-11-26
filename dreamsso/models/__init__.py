
import logging
from django.contrib.auth.models import Permission

userdb_installed = False

l = logging.getLogger(__name__)


def _get_or_create_perm(perm):
  from django.contrib.contenttypes.models import ContentType
  from django.db import models
  if not perm:
    return None
  try:
    app, model, name = perm.split('.')
  except ValueError:
    return None
  # NOTE: This check is added to support local userdb database connection.
  # TODO: Ensure this is right.
  m = models.get_model(app, model, only_installed=False)
  if not m:
    return None
  try:
    return Permission.objects.get_by_natural_key(name, app, model)
  except Permission.DoesNotExist:
    try:
      ct = ContentType.objects.get_by_natural_key(app, model)
      perm = Permission(name=name, content_type=ct, codename=name)
      perm.save()
      return perm
    except ContentType.DoesNotExist:
      return None
  except ContentType.DoesNotExist:
    return None


from django.conf import settings

if 'dreamuserdb' in settings.INSTALLED_APPS:
  from dreamsso.models.local import User, Group, Role
else:
  from dreamsso.models.remote import User
  # TODO Remote access for Group and Role not implemented

__all__ = ['User']
