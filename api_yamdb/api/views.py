from rest_framework.pagination import LimitOffsetPagination
from .permissions import OwnerOrReadOnly
from .serializers import CommentsSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .filters import TitleFilter
from .mixins import ListCreateDestroyMixins
from .permissions import IsAdminAuthorModeratorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, GenreSerializer, ReviewSerializer,
    TitleWriteSerializer, TitleReadSerializer
)
from reviews.models import Category, Genre, Title, Comments, Review, User


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (OwnerOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, review_id=review_id, )
        new_queryset = Comments.objects.filter(review_id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post")
        get_object_or_404(Review, id=post_id)
        serializer.save(author=self.request.user, post_id=post_id)


class GenreCategoryViewSet(
        ListCreateDestroyMixins,
        viewsets.GenericViewSet
        ):
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
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
