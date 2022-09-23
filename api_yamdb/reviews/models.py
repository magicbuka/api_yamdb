from datetime import datetime
import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import username_validator

CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)
CODE_LENGTH = 6


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(max_length=254, unique=True)
    role = models.CharField(
        max_length=max([len(a[0]) for a in CHOICES]),
        choices=CHOICES,
        default=CHOICES[0][0]
    )
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_superuser = models.BooleanField(default=False)
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        blank=True,
        default=''
    )

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('username',)

    def is_admin(self):
        return (
            self.is_superuser
            or self.is_staff
            or (self.role == CHOICES[2][0])
        )

    def is_moderator(self):
        return self.is_admin() or (self.role == CHOICES[1][0])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class CategoryGenreModel(models.Model):
    name = models.TextField(
        'Название',
        max_length=256
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        max_length=50
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return f'Название - {self.name}'


class Category(CategoryGenreModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        verbose_name='Название',
        blank=False
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(datetime.now().year)
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class ReviewCommentModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(ReviewCommentModel):
    MESSAGE_FORM = (
        'Произведение: {}, '
        'отзыв: {}, '
        'автор отзыва: {}, '
        'оценка: {}, '
        'дата публикации отзыва: {}.'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        verbose_name='Оценка'
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                name='Проверка уникальности отзыва',
                fields=['author', 'title']
            ),
        ]

    def __str__(self):
        return self.MESSAGE_FORM.format(
            self.title,
            self.text{:.15},
            self.author,
            self.score,
            self.pub_date
        )


class Comment(ReviewCommentModel):
    MESSAGE_FORM = (
        'Текст комментария: {}, '
        'автор: {}, '
        'обзор: {}, '
        'дата публикации отзыва: {}.'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.MESSAGE_FORM.format(
            self.text{:.15},
            self.author,
            self.review{:.15},
            self.pub_date
        )
