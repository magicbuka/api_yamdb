from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import User


class NoMeUsername:
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, attrs, *args, **kwargs):
        if attrs['username'] == 'me':
            raise ValidationError(self.message, code='unique')


class ChekCode:
    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, attrs, *args, **kwargs):
        user = User.objects.get(username=attrs['username'])
        if user.confirmation_code != attrs['confirmation_code']:
            raise ValidationError(self.message, code='unique')
