
import dreamuserdb.models
from dreamsso.models import _get_or_create_perm


class User(dreamuserdb.models.User):
  """ Implements the dreamsso.models.User interface
  by accessing the userdb database directly without any API
  """
  class Meta:
    proxy = True
    app_label = 'dreamsso'

  def update(self, data):
    self.save()

  def save(self, commit_userdb=True, *args, **kwargs):
      super(User, self).save(*args, **kwargs)

  def belongs_to_organisation(self, id):
    return self.organisations.filter(pk=id).count() > 0

  def belongs_to_role(self, id):
    return self.roles.filter(pk=id).count() > 0

  def belongs_to_group(self, id):
    return self.user_groups.filter(pk=id).count() > 0

  @property
  def usergroups(self):
    return self.user_groups.all().values('id')

  def update_permissions_from_roles(self):
    perms = list()
    for role in self.roles.all():
      for serviceperm in role.permissions.all():
        perm_str = '%s.%s.%s' % (serviceperm.service, serviceperm.entity, serviceperm.action)
        perm = _get_or_create_perm(perm_str)
        if perm:
            perms.append(perm)
    self.user_permissions.clear()
    self.user_permissions.add(*perms)
    self.save()


class Group(dreamuserdb.models.Group):

  class Meta:
    proxy = True
    app_label = 'dreamsso'


class Role(dreamuserdb.models.Role):

  class Meta:
    proxy = True
    app_label = 'dreamsso'

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

