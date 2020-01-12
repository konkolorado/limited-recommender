from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_all_digits(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s should be composed of only digits'),
            params={'value': value},
        )
