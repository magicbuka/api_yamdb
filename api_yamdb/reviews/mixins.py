from rest_framework.exceptions import ValidationError
import re


WRONG_USERNAME = 'Недопустимое имя пользователя!'


class UsernameMixins:
    pass

    def validate_username(self, value):
        """
        username != 'me'
        username includes only letters, digits and @/./+/-/_
        """
        if value == 'me' or not re.compile(r'^[\w.@+-]').match(value):
            raise ValidationError(WRONG_USERNAME, code='unique')
        return value
