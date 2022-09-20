from .validators import NoMeUsername, ChekUserCode
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from rest_framework import serializers

from .validators import ChekUserCode, NoMeUsername

from reviews.models import Category, Comments, Genre, Review, Title, User

MORE_THAN_ONE_REVIEW = 'Превышено допустимое количество отзывов. Разрешен один на одно произведение.'
WRONG_CODE = 'Неправильный код!'
WRONG_USERNAME = 'Недопустимое имя пользователя!'


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Создание нового пользователя
    """
    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )
        validators = [
           NoMeUsername(
                fields=('username',),
                message=WRONG_USERNAME
            ),
        ]


class TokenSerializer(serializers.Serializer):
    """
    Проверка кода подтверждения по имени пользователя
    """
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField(max_length=6)

    class Meta:
        validators = [
            ChekUserCode(
                fields=('username',),
                message=WRONG_CODE
            ),
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Работа Администратора с пользователями
    """
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        optional_fields = ('first_name', 'last_name', 'bio', 'role')


class MeSerializer(UserSerializer):
    """
    Работа с собственной учетной записью
    """
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CommentsSerializer(serializers.ModelSerializer):
    """
    Комментарии к отзывам
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments


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
