# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
import os

from django.conf import settings

STATICFILES_DIRS = [os.path.join('markup/static/')]
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(settings.BASE_DIR, '../static')
MEDIA_ROOT = os.path.join(settings.BASE_DIR, '../static', 'media/')
MEDIA_URL = '/media/'
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
