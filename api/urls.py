from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    send_confirmation_code,
    get_user_token,
    UserViewSet,
    UserInfo,
    GenreViewSet,
    CategoriesViewSet,
    TitleViewSet,
    ReviewCommentDetailViewSet,
    ReviewDetailViewSet,
)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoriesViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewDetailViewSet, basename='review')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/('
                   r'?P<review_id>\d+)/comments',
                   ReviewCommentDetailViewSet, basename="reviews_comments")

urlpatterns = [
    path('v1/auth/email/', send_confirmation_code),
    path('v1/auth/token/', get_user_token),
    path('v1/users/me/', UserInfo.as_view()),
    path('v1/', include(v1_router.urls))
]
