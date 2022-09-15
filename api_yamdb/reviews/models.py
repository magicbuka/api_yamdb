from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


CHOICES = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=1, choices=CHOICES, default='u')
    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'


class Review(models.Model):
    pass


class Comments(models.Model):
    review_id = models.ForeignKey(Review,
                                  on_delete=models.CASCADE,
                                  related_name='Comments'
                                  )
    text = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='Comments'
                               )
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    )
