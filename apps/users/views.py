from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.views import ExtendedViewSet
from apps.users.serializers import UserRegisterSerializer, UserListSerializer

User = get_user_model()

__all__ = (
    "UserViewSet",
)


class UserViewSet(ExtendedViewSet, ListModelMixin):
    queryset = User.objects.all()
    permission_by_action = {
        "register": [AllowAny],
        "list": [IsAdminUser],
    }
    serializers_by_action = {
        "default": UserListSerializer,
        "register": UserRegisterSerializer,
        "list": UserListSerializer,
    }

    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="user-register",
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email", None)
        password = serializer.validated_data.get("password", None)
        user = serializer.save(username=email)
        user.set_password(password)
        user.save()
        refresh: RefreshToken = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
