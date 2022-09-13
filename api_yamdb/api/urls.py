from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'posts/(?P<post>[^/.]+)/comments',
                CommentViewSet,
                basename='comments'
                )

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
