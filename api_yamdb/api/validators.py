from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import User


class ChekUserCode:
    """
    Проверка правильности кода подтверждения из email
    """
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, attrs, *args, **kwargs):
        user = get_object_or_404(User, username=attrs['username'])
        if user.confirmation_code != attrs['confirmation_code']:
            raise ValidationError(self.message, code='unique')
