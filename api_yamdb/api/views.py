from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

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

    def get_queryset(self):
        post_id = self.kwargs.get("post")
        get_object_or_404(Review, id=post_id)
        new_queryset = Comments.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post")
        get_object_or_404(Review, id=post_id)
        serializer.save(author=self.request.user, post_id=post_id)
