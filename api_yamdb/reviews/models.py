from django.contrib.auth.models import AbstractUser
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


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


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
    year = models.IntegerField(verbose_name='Год')
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


class Review(models.Model):
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
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Отзыв',
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
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


class Comment(models.Model):
    MESSAGE_FORM = (
        'отзыв: {}, '
        'текст: {}, '
        'автор комментария: {}, '
        'дата публикации комментария: {}.'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.MESSAGE_FORM.format(
            self.review,
            self.text[:75] + '..',
            self.author,
            self.pub_date
        )
