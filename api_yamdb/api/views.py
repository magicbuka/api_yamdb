from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comments, Review
from .permissions import OwnerOrReadOnly
from .serializers import CommentsSerializer, UserSerializer

User = get_user_model()


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
