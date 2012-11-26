
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from dreamsso import userdb
from dreamsso.models import _get_or_create_perm

userdb_installed = False

l = logging.getLogger(__name__)

# TODO Create cron job which cleans the local db of stale user objects
# This is the same as removing expired sessions

class UserManager(models.Manager):
  def get_userdb(self, **kwargs):
    """ Get user from UserDB and update local instance.

    Supports 'id' argument. With other query types raises NotImplementedError.
    """
    user = None
    data = {}

    if 'id' in kwargs:
      data = userdb.User(kwargs['id']).get()
    else:
      raise NotImplementedError

    if not data:
        raise ObjectDoesNotExist('No user found in userdb with id %d' % kwargs.get('id'))

    user, created = User.objects.get_or_create(id=data['id'], username=data['username'])
    user.update(data)
    d = {}
    for p in getattr(user, 'saml_permissions', []):
      if p.find('.') == -1:
        continue
      org, role, perm = p.split('.', 2)
      role = org+'.'+role
      perm = _get_or_create_perm(perm)
      if perm:
        if not role in d:
          d[role] = []
        d[role].append(perm)
    groups = []
    for saml_role in getattr(user, 'saml_roles', []):
      org, role = saml_role.split('.')
      group, created = Group.objects.get_or_create(id=role, name=saml_role)
      if saml_role in d:
        group.permissions = d[saml_role]
      else:
        group.permissions = []
      group.save()
      groups.append(group)
    user.groups = groups
    user.save()
    l.debug('User %s'%user, extra={'data':{'user': repr(user)}})
    # TODO For some reason this print didn't work
#    l.debug('User %s'%user, extra={'data':{
#      'attributes':user._data,
#      'permissions':user.get_all_permissions(),
#      'groups':user.groups.all(),
#      }})
    return user


class User(DjangoUser):
  class Meta:
    proxy = True

  objects = UserManager()

  def update(self, data):
    if self._update(data):
      self.save()

  def belongs_to_organisation(self, id):
    orgs = [o[u'id'] for o in self.organisations]
    return int(id) in orgs

  def belongs_to_role(self, id):
    roles = [o[u'id'] for o in self.roles]
    return int(id) in roles

  def belongs_to_group(self, id):
    groups = [o[u'id'] for o in self.usergroups]
    return int(id) in groups

  def dummy_update(self):
    import json
    import codecs
    from django.conf import settings
    fn = getattr(settings, 'DS_DUMMY_USERDATA_FILE', None)
    if not fn:
      return
    f = codecs.open(fn)
    if self._update(json.load(f)):
      self.save()
    f.close()

  def _update(self, data):
    if not data:
      data = {}
    if 'groups' in data:
      # Need to rename groups variable coming from
      # UserDb as the same field is used by django
      # to handle permission groups
      data['usergroups'] = data['groups']
      del data['groups']
    need_save = False
    for key in ['username', 'first_name', 'last_name', 'email']:
      if key in data and getattr(self, key) != data[key]:
        need_save = True
        setattr(self, key, data.get(key, None))
    self.__dict__['_data'] = data
    return need_save

  def __getattr__(self, name):
    if '_data' in self.__dict__:
      if name in self.__dict__['_data']:
        return self.__dict__['_data'][name]
    return super(User, self).__getattribute__(name)

  def __setattr__(self, name, value):
    #NOTE when altering attributes directly, ie user.usergroup.append('foo'), the '_changed' tracking
    #breaks. __setattr__ is called only when assigning to attribute. ie user.usergroups = ['foo']
    if '_data' in self.__dict__:
      if name in ['password'] or (name in self.__dict__['_data'] and self.__dict__['_data'][name] != value):
        if not '_changed' in self.__dict__:
          self.__dict__['_changed'] = {}
        self.__dict__['_changed'][name] = True
      self.__dict__['_data'][name] = value
    super(User, self).__setattr__(name, value)

  def save(self, *args, **kwargs):
    commit_userdb = kwargs.pop('commit_userdb', False)
    super(User, self).save(*args, **kwargs)
    if commit_userdb:
      changed = self.__dict__.get('_changed', {}).keys()
      data = self.__dict__.get('_data', {})
      l.debug('User.save(commit_userdb=True): %s'%repr(changed), extra={'data': {'changed': changed, 'data': data}})
      if len(changed):
        changed_data = {}
        for key in changed:
          if key in data:
            if key == 'usergroups':
              changed_data['groups'] = data[key]
            else:
              changed_data[key] = data[key]
        if len(changed_data):
          l.debug('Committing data to userdb: %s'%repr(changed_data))
          userdb.User(self.id).update(**changed_data)

