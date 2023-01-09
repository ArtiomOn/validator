from rest_framework.routers import DefaultRouter

from apps.validations.views import EmailViewSet, IMEIViewSet, JwtTokenViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"email", EmailViewSet)
router.register(r"imei", IMEIViewSet)
router.register(r"jwt_token", JwtTokenViewSet)

urlpatterns = router.urls
