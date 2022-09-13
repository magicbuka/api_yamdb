from rest_framework.exceptions import ValidationError


class NotEqualFields:
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, attrs, *args, **kwargs):
        checked_values = []
        for field, value in attrs.items():
            if field in self.fields:
                checked_values.append(value)
        if checked_values[0] == checked_values[1]:
            field_names = ', '.join(self.fields)
            message = self.message.format(field_names=field_names)
            raise ValidationError(message, code='unique')
