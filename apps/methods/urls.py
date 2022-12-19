from rest_framework.routers import DefaultRouter

from apps.methods.views import EmailViewSet, IMEIViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'email', EmailViewSet)
router.register(r'imei', IMEIViewSet)

urlpatterns = router.urls
