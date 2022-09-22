from rest_framework.exceptions import ValidationError
import re

WRONG_USERNAME = 'Недопустимое имя пользователя!'


def username_validator(value):
    """
    username != 'me'
    username includes only letters, digits and @/./+/-/_
    """
    print('ffff')
    if value == 'me' or (not re.compile(r'^[\w.@+-]').match(value)):
        raise ValidationError(WRONG_USERNAME, code='unique')
    return value
