from datetime import datetime
import re

from rest_framework.exceptions import ValidationError

WRONG_USERNAME = '"me" - недопустимое имя пользователя!'
WRONG_SYMBOLS = "Недопустимые символы: {}"
WRONG_YEAR = (
    'Недопустимое значение поля "Год"! '
    'Указанное значение: {} превышает значение текущего года: {}'
)


def username_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    if value == 'me':
        raise ValidationError(WRONG_USERNAME)
    if not re.fullmatch(r'^[\w.@+-]+', value):
        raise ValidationError(
            WRONG_SYMBOLS.format(
                "".join(set(re.findall(r"[^\w.@+-]", value)))
            )
        )
    return value


def year_validator(value):
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(WRONG_YEAR.format(value, current_year))
    return value
