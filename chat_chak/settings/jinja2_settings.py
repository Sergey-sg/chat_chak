import jinja2
from django.conf import settings
from django_jinja.builtins import DEFAULT_EXTENSIONS

settings.TEMPLATES += {
    'BACKEND': 'django_jinja.backend.Jinja2',
    'NAME': 'jinja2',
    'APP_DIRS': True,
    'DIRS': ['markup/templates/'],
    'OPTIONS': {
        'environment': 'shared.env.jinja2.environment',
        'match_extension': '.jinja2',
        'newstyle_gettext': True,
        'auto_reload': True,
        'undefined': jinja2.Undefined,
        'debug': True,

        'filters': {},

        "globals": {
            'available_languages': 'shared.templatetags.language.get_lang_urls',
        },

        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ],

        'extensions': DEFAULT_EXTENSIONS,

        "bytecode_cache": {
            "name": "default",
            "backend": "django_jinja.cache.BytecodeCache",
            "enabled": True,
        },
    },
},
