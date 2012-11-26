
from django.conf import settings

USERDB_ENDPOINT = getattr(settings, 'USERDB_ENDPOINT', 'http://127.0.0.1:8000/api/1')
USERDB_USER = getattr(settings, 'USERDB_USER', '')
USERDB_PASSWORD = getattr(settings, 'USERDB_PASSWORD', '')

USE_CACHE = getattr(settings, 'DREAMSSO_USE_USERDB_CACHE', False)
