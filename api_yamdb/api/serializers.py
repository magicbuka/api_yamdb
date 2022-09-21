from .validators import ChekUserCode
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Genre, Review, Title, Comment, User
from rest_framework.exceptions import ValidationError


MORE_THAN_ONE_REVIEW = (
    'Превышено допустимое количество отзывов. '
    'Разрешен один на одно произведение.'
)
WRONG_CODE = 'Неправильный код!'
WRONG_USERNAME = 'Недопустимое имя пользователя!'


class CreateUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(WRONG_USERNAME, code='unique')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        validators = [
            ChekUserCode(
                fields=('username', 'confirmation_code'),
                message=WRONG_CODE
            ),
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        optional_fields = ('first_name', 'last_name', 'bio', 'role')


class MeSerializer(UserSerializer):
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
    category = CategorySerializer()
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'genre', 'year',
            'category', 'description', 'rating'
        )

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


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
        fields = '__all__'


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
        read_only_fields = ('title',)
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
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
        read_only_fields = ('review',)
        fields = '__all__'
