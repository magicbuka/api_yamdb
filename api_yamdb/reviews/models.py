from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.conf import settings
from .validators import username_validator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
CHOICES = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)



class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=len(max(role[0] for role in CHOICES)),
        choices=CHOICES,
        default=USER
    )
    bio = models.TextField('О себе', blank=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        blank=True,
        default=''
    )

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('username',)

    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    def is_moderator(self):
        return self.role == MODERATOR

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
        'отзыв: {:.15}, '
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
            self.text,
            self.author,
            self.score,
            self.pub_date
        )


class Comment(ReviewCommentModel):
    MESSAGE_FORM = (
        'Текст комментария: {:.15}, '
        'автор: {}, '
        'обзор: {:.15}, '
        'дата публикации отзыва: {}.'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарий',
    )

    class Meta(ReviewCommentModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.MESSAGE_FORM.format(
            self.text,
            self.author,
            self.review,
            self.pub_date
        )
