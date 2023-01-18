from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

PHONE_REGEX = RegexValidator(
        regex=r'^\+380\d{9}',
        message=_('The phone number must be in the format: "+380999999999". Starts with "+380" and 9 digits.')
)
