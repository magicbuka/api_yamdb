from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from django.conf import settings
from .mixins import UsernameMixins
from reviews.models import Category, Comment, Genre, Review, Title, User

MORE_THAN_ONE_REVIEW = (
    'Превышено допустимое количество отзывов. '
    'Разрешен один на одно произведение.'
)


class GetOrCreateUserSerializer(serializers.Serializer, UsernameMixins):
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
    username = serializers.CharField(max_length=settings.USERNAME_MAX_LENGTH)


class ConfCodeSerializer(serializers.Serializer, UsernameMixins):
    username = serializers.CharField(max_length=settings.USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH
    )


class UserSerializer(serializers.ModelSerializer, UsernameMixins):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        optional_fields = ('first_name', 'last_name', 'bio', 'role')


class MeUserSerializer(UserSerializer, UsernameMixins):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        FIELDS = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title
        fields = FIELDS
        read_only_fields = FIELDS


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author',
            'score', 'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            title=get_object_or_404(
                Title,
                id=self.context['view'].kwargs.get('title_id')
            ),
            author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(MORE_THAN_ONE_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
