from rest_framework import routers

from apps.users.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', UserViewSet, basename='user')

urlpatterns = router.urls
