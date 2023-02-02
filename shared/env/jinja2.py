from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django.contrib.staticfiles.storage import staticfiles_storage
from jinja2 import Environment


def environment(**options):
    """
    Provides default environment for jinja.
    """
    options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        "crispy": as_crispy_form,
    })
    return env
