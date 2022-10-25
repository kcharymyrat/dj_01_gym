from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ImproperlyConfigured

PROTECTED_MEDIA = getattr(settings, "PROTECTED_MEDIA", None)

if not PROTECTED_MEDIA:
    raise ImproperlyConfigured("PROTECTED_MEDIA is not propertly configured")

class ProtectedStorage(FileSystemStorage):
    location = PROTECTED_MEDIA