from rest_framework.routers import DefaultRouter

from apps.temp_mail.views import TempMailViewSet, MessageViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'temp_mail', TempMailViewSet, basename='temp_mail')
router.register(r'message', MessageViewSet, basename='temp_mail')

urlpatterns = router.urls
