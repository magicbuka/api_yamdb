from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateUserViewSet, token_view, me_view, UsersViewSet,
                    CommentViewSet,  CategoryViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet
                    )

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('auth/signup', CreateUserViewSet, basename='signup')
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


urlpatterns = [
    path('v1/auth/token/', token_view, name='token'),
    path('v1/users/me/', me_view),
    path('v1/', include(router_v1.urls)),
]
