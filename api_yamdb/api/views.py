import random

from django.db.utils import IntegrityError
from django.db.models.aggregates import Avg
from django.conf import settings
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
from django.http import JsonResponse

from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly, IsAdmin, IsAdminAuthorModeratorOrReadOnly
)
from .serializers import (
    GetOrCreateUserSerializer, CategorySerializer,
    GenreSerializer, MeUserSerializer,
    ReviewSerializer, TitleWriteSerializer,
    TitleReadSerializer, ConfCodeSerializer,
    CommentSerializer, UserSerializer
)
from reviews.models import Category, Genre, Review, Title, User

WRONG_USERNAME_EMAIL = 'Некорректные поля: {}'
WRONG_CODE = 'Неправильный код!'


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_view(request):
    serializer = GetOrCreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email']
        )
    except IntegrityError as e:
        raise ValidationError(WRONG_USERNAME_EMAIL.format(e))
    user.confirmation_code = ''.join(
        random.sample(
            settings.CONFIRMATION_CODE_SET,
            settings.CONFIRMATION_CODE_LENGTH
        )
    )
    user.save()
    send_mail(
        'Активация аккаунта',
        f'Ваш код активации: {user.confirmation_code}',
        settings.FROM_EMAIL,
        [user.email]
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        headers=serializer.data
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token_view(request):
    serializer = ConfCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data['username'])
    code = user.confirmation_code
    user.confirmation_code = ''
    user.save()
    if code != serializer.data['confirmation_code'] or code == '':
        raise ValidationError(WRONG_CODE)
    token = RefreshToken.for_user(user)
    return JsonResponse({"token": str(token)}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    lookup_field = 'username'


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me_view(request):
    if request.method == 'GET':
        return Response(
            MeUserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )
    serializer = MeUserSerializer(
        request.user,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering = ('name')
    ordering_fields = ('name',)

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
