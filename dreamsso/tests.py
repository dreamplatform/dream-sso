
from django.test import TransactionTestCase

class SamlBackendTestCase(TransactionTestCase):
  fixtures = ['dream_sso_test.json']

  def xtestLogin(self):
    from dream_sso.authbackend import SamlBackend
    b = SamlBackend()
    u = False #b.authenticate('testatep', 't')
    if not u:
      print "Authentication failed. Connection problems, perhaps?"

class UserDbClientTestCase(TransactionTestCase):
  
  def xtestChangeThemeColor(self):
    from dream_sso.userdb import User
    print User(1).get()
    print User(1).update(theme_color='121212')

