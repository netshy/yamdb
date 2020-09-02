# Import all from normal settings
from .settings import *

# Delete postgres database
DATABASES.pop('default')

# Use sqlite3 for correct test
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
