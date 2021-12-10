from django.urls import path, include
from .views import BroilerViewSet, UserViewSet, InventoryWeekViewSet, NotificationViewSet
from rest_framework_simplejwt import views as jwt_views
from api.views import LogoutAndBlacklistRefreshTokenForUserView

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('broilers', BroilerViewSet, basename='broilers')
router.register('users', UserViewSet, basename='users')
router.register('weeks', InventoryWeekViewSet, basename='weeks')
router.register('notifications', NotificationViewSet, basename='notifications')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('api/auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
]
