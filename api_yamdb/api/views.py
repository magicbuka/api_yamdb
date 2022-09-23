import json
import random
import string

from django.db.utils import IntegrityError
from django.db.models.aggregates import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly, IsAdmin, IsAdminAuthorModeratorOrReadOnly
)
from .serializers import (
    CreateUserSerializer, CategorySerializer,
    GenreSerializer, MeSerializer,
    ReviewSerializer, TitleWriteSerializer,
    TitleReadSerializer, TokenSerializer,
    CommentSerializer, UserSerializer
)
from reviews.models import Category, CODE_LENGTH, Genre, Review, Title, User


WRONG_USERNAME_EMAIL = 'Некорректные поля!'
WRONG_CODE = 'Неправильный код!'


def generate_activation_code(user):
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits
    ) for x in range(CODE_LENGTH))


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_view(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email']
        )
    except IntegrityError:
        raise ValidationError(WRONG_USERNAME_EMAIL, code='unique')
    user.confirmation_code = generate_activation_code(user)
    user.save()
    send_mail(
        'Activate Your Account',
        f'Here is the activation code: {user.confirmation_code}',
        'admin@yamdb.fake',
        [user.email]
    )
    headers = serializer.data
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        headers=headers
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token_view(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data['username'])
    if user.confirmation_code != serializer.data['confirmation_code']:
        user.confirmation_code = ''
        raise ValidationError(WRONG_CODE, code='unique')
    token = RefreshToken.for_user(user)
    return Response(
        json.loads(json.dumps({'token': str(token.access_token)})),
        status=status.HTTP_200_OK
    )


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me_view(request):
    if request.method == 'GET':
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = MeSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreCategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GenreCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return Title.objects.all().annotate(
            rating=Avg('reviews__score'),
        ).order_by('rating')

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminAuthorModeratorOrReadOnly
    )

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminAuthorModeratorOrReadOnly
    )

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
