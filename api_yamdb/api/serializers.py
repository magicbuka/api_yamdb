from rest_framework import serializers

from reviews.models import Comments, User
from djoser.serializers import UserCreateSerializer
from .validators import NoMeUsernaem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'username',
        )
        validators = [
           NoMeUsernaem(
                fields=('username',),
                message='Недопустимое имя пользователя!'
            ),
        ]
