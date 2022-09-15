from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, UsersViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
                CommentViewSet,
                basename='comments'
                )
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token', views.obtain_auth_token, name='token'),
    path('v1/auth/signup/', UserViewSet.as_view({'post': 'create'}), name="signup"),
    path('v1/', include(router.urls)),
]
