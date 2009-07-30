from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    from django.utils.importlib import import_module
except ImportError:
    "django.utils.importlib is only available in django 1.1 onwards"
    def import_module(name):
        return __import__(name, '', '', [''])

from crowdsource.forms import CrowdSourcedEntryForm

def get_form():
    if hasattr(settings, 'CROWD_SOURCED_ENTRY_FORM_MODULE'):
        try:
            package = import_module(getattr(settings, 'CROWD_SOURCED_ENTRY_FORM_MODULE'))
        except ImportError:
            raise ImproperlyConfigured("The CROWD_SOURCED_ENTRY_FORM_MODULE setting "\
                                       "refers to a non-existing package.")
        if hasattr(settings, 'CROWD_SOURCED_ENTRY_FORM_NAME'):
            try:
                cls = getattr(package, getattr(settings, 'CROWD_SOURCED_ENTRY_FORM_NAME'))
            except AttributeError:
                raise ImproperlyConfigured("The class defined in the CROWD_SOURCED_ENTRY_FORM_MODULE "\
                                "setting cannot be imported. Make sure the CROWD_SOURCED_ENTRY_FORM_NAME "\
                                "setting is correct.")
        return cls
    else:
        return CrowdSourcedEntryForm
