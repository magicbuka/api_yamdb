from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (CommentViewSet, UsersViewSet,
                    CategoryViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet
                    )

app_name = 'api'

router = DefaultRouter()
router.register(r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
                CommentViewSet,
                basename='comments'
                )
router.register('users', UsersViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')

urlpatterns = [
    path('v1/auth/token', TokenObtainPairView.as_view(), name='token'),
    #path('v1/auth/signup/', , name="signup"),
    path('v1/', include(router.urls)),
]
