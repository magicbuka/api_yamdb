from datetime import datetime
import re

from rest_framework.exceptions import ValidationError

WRONG_USERNAME = 'Недопустимое имя пользователя!'
WRONG_YEAR = (
    'Недопустимое значение поля "Год"! '
    'Указанное значение: {}, превышает текущее: {}'
)


def username_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    if value == 'me' or not re.fullmatch(r'^[\w.@+-]+', value):
        raise ValidationError(WRONG_USERNAME, code='unique')
    return value


def year_validator(value):
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(WRONG_YEAR.format(value, current_year))
