import datetime
import re
from django.core.exceptions import ValidationError


def validate_year(value):
    year_today = datetime.date.today().year
    if value > year_today:
        raise ValidationError(("Год произведения не может быть в будущем"))
    return value


def validate_slug(value):
    if re.match(pattern=r"^[-a-zA-Z0-9_]+$", string=value):
        return value
    raise ValidationError(
        "В поле Slug содержится запрещенные символы"
    )