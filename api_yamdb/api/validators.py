from rest_framework.exceptions import ValidationError


class NoMeUsernaem:
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, attrs, *args, **kwargs):
        if attrs['username'] == 'me':
            raise ValidationError(self.message, code='unique')
