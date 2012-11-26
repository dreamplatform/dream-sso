
import logging
import json
import urllib2
import hashlib
from django.core.cache import cache
import settings

class UserDbGeneralException(Exception):
  pass

l = logging.getLogger(__name__)

class Client(object):
  def __init__(self):
    pwmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pwmgr.add_password(None, settings.USERDB_ENDPOINT, settings.USERDB_USER, settings.USERDB_PASSWORD)
    handler = urllib2.HTTPBasicAuthHandler(pwmgr)
    self.urlopen = urllib2.build_opener(handler)

  def _get(self, args, kwargs={}, refresh_cache=False):
    url = self._build_url(args, kwargs)
    cache_in_use = settings.USE_CACHE and not refresh_cache
    if cache_in_use:
      key = self._build_key(url)
      data = cache.get(key)
      if data:
        l.debug('UserDb Client. Get from CACHE', extra={'data':{'endpoint':url, 'key' : key}})
        return data
    l.debug('UserDB API GET as %s'%settings.USERDB_USER, extra={'data':{'endpoint':url}})
    try:
      data = self.urlopen.open(urllib2.Request(url)).read()
      d = json.loads(data)
      if settings.USE_CACHE:
        cache.set(key, d)
      return d
    except (urllib2.URLError, RuntimeError):
      l.exception('Userdb get failed')
      return None

  def _put(self, args, data, kwargs={}):
    url = self._build_url(args, kwargs)
    l.debug('UserDB API PUT as %s'%settings.USERDB_USER, extra={'data':{'endpoint':url, 'data':data}})
    try:
      request = urllib2.Request(url=url, data=json.dumps(data))
      request.add_header('Content-Type', 'application/json')
      request.get_method = lambda: 'PUT'
      result = self.urlopen.open(request).read()
      if settings.USE_CACHE:
        #TODO clearing whole cache is bit overkill, but finer cache invalidation is hard to
        #implement
        cache.clear()
      return result
    except (urllib2.HTTPError, urllib2.URLError, RuntimeError):
      l.exception('Userdb put failed')
      return None

  def _build_url(self, args, kwargs):
    args = [unicode(a) for a in args]
    url = '%s/%s/' % (settings.USERDB_ENDPOINT, '/'.join(args))
    if len(kwargs):
      url += '?'+'&'.join(['%s=%s'%(k,v) for k,v in kwargs.iteritems()])
    return url

  def _build_key(self, url):
    """
    Builds cache key from full url. url is pre build full url from args and
    kwargs (string).
    """
    return hashlib.md5(url).hexdigest()


class User(Client):
  def __init__(self, id=None):
    self.id = str(id)
    super(User, self).__init__()

  def get(self):
    return self._get(('user', self.id))

  def update(self, **data):
    return self._put(('user', self.id), data)

  def authenticate(self, username, password):
    return self._get(('authenticate',), {'username':username, 'password':password})

