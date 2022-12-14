from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from apps.users.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', UserViewSet, basename='user')

urlpatterns = router.urls

urlpatterns += [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/access/', TokenObtainPairView.as_view(), name='token_access'),
]
