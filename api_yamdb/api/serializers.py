from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.mixins import UsernameMixins
from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import ChekUserCode, NoMeUsername

MORE_THAN_ONE_REVIEW = (
    'Превышено допустимое количество отзывов. '
    'Разрешен один на одно произведение.'
)


class CreateUserSerializer(serializers.Serializer, UsernameMixins):
    email = serializers.EmailField()
    username = serializers.CharField()


class TokenSerializer(serializers.Serializer, UsernameMixins):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer, UsernameMixins):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        optional_fields = ('first_name', 'last_name', 'bio', 'role')


class MeSerializer(UserSerializer, UsernameMixins):
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
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'name', 'genre', 'year',
            'category', 'description', 'rating'
        )


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
        read_only_fields = ('id', 'author', 'pub_date')
        fields = ('id', 'text', 'author', 'pub_date')
