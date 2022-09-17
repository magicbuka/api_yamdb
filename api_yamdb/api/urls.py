from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (token_view, CreateUserViewSet, MeUserViewSet,
                    UsersViewSet, CommentViewSet,  CategoryViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet,
                    )

app_name = 'api'

router = DefaultRouter()
router.register('auth/signup', CreateUserViewSet, basename='signup')
router.register('users/me', MeUserViewSet, basename='meuser')
router.register('users', UsersViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='reviews'
                )
router.register(r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments',
                CommentViewSet,
                basename='comments'
                )


urlpatterns = [
    path('v1/auth/token/', token_view, name='token'),
    path('v1/', include(router.urls)),
]
