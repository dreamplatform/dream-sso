
from django.contrib.auth.backends import ModelBackend
from dreamsso.models import User

class LocalBackend(ModelBackend):
  def authenticate(self, username=None, password=None, **kwargs):
    try:
      if username:
        user = User.objects.get(username=username)
        if user.check_password(password):
          user.update_permissions_from_roles()
          return user
    except User.DoesNotExist:
      pass
    return None

  def get_user(self, user_id):
    try:
      user = User.objects.get(pk=user_id)
      user.update_permissions_from_roles()
      return user
    except User.DoesNotExist:
      return None

