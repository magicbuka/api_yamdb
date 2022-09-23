from rest_framework.exceptions import ValidationError
import re

WRONG_USERNAME = 'Недопустимое имя пользователя!'


def username_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    if value == 'me' or not re.fullmatch(r'^[\w.@+-]+', value):
        raise ValidationError(WRONG_USERNAME, code='unique')
    return value
