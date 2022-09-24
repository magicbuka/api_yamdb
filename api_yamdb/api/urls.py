from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    create_user_view,
    CommentViewSet, CategoryViewSet,
    GenreViewSet, me_view,
    ReviewViewSet, TitleViewSet, token_view,
    UsersViewSet
)


router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/'
    r'(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth = [
    path('auth/signup/', create_user_view, name='signup'),
    path('auth/token/', token_view, name='token'),
]
urlpatterns = [
    path('v1/', include(auth)),
    path('v1/users/me/', me_view),
    path('v1/', include(router_v1.urls)),
]
