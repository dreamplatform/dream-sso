
import logging
from django.contrib.auth.backends import ModelBackend
from dreamsso.models import User

LOG = logging.getLogger(__name__)

class DummyLocalBackend(ModelBackend):
  def authenticate(self, **kwargs):
    user = super(DummyLocalBackend, self).authenticate(**kwargs)
    return user

  def get_user(self, user_id):
    user,created = User.objects.get_or_create(id=user_id)
    user.dummy_update()
    user.save()
    LOG.debug("Dummy auth with user %s" % user)
    return user

class DummyUserDbBackend(ModelBackend):
  def authenticate(self, **kwargs):
    from dreamsso import userdb
    data = userdb.User().authenticate(**kwargs)
    user = self.get_user(data['id'])
    return user

  def get_user(self, user_id):
    user = User.objects.get_userdb(id=user_id)
    LOG.debug("Dummy auth with user %s" % user)
    return user

