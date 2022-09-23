from rest_framework.exceptions import ValidationError
import re

WRONG_USERNAME = '"me" - недопустимое имя пользователя!'
WRONG_SYMBOLS = 'Допустимы только буквы, цифры, "@", ".", "+", "-" и "_".'


def username_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    if value == 'me':
        raise ValidationError(WRONG_USERNAME)
    if not re.fullmatch(r'^[\w.@+-]+', value):
        raise ValidationError(WRONG_SYMBOLS)
    return value
