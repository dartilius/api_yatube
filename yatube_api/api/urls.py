from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, GroupViewSet, CommentViewSet

router = SimpleRouter()
router_comments = SimpleRouter()

router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router_comments.register('comments', CommentViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/posts/<int:post_pk>/', include(router_comments.urls))
]
