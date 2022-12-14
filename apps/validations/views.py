from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from apps.common.views import ExtendedRetrieveUpdateDestroyAPIView, ExtendedListAPIView
from apps.validations.generators.imei_generator import ImeiGenerator
from apps.validations.generators.jwt_generator import JWTGenerator
from apps.validations.models import Email, IMEI, JwtToken
from apps.validations.serializers import (
    EmailSerializer,
    IMEISerializer,
    JwtTokenEncodeSerializer,
    JwtTokenDecodeSerializer,
)

__all__ = [
    "EmailViewSet",
    "IMEIViewSet",
    "JwtTokenViewSet",
]


# noinspection DuplicatedCode
class EmailViewSet(ExtendedRetrieveUpdateDestroyAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_by_action = {
        "default": [IsAuthenticated],
        "delete": [IsAdminUser],
        "update": [IsAdminUser],
    }

    @action(detail=False, methods=["post"], url_path="email_check", url_name="email_check")
    def email_check(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(
                is_valid=True,
                user=request.user,
            )
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="user_email", url_name="user_email")
    def user_email(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# noinspection DuplicatedCode
class IMEIViewSet(ExtendedRetrieveUpdateDestroyAPIView):
    queryset = IMEI.objects.all()
    serializers_by_action = {
        "default": IMEISerializer,
    }
    permission_by_action = {
        "default": [IsAuthenticated],
        "generate_imei": [AllowAny],
        "delete": [IsAdminUser],
        "update": [IsAdminUser],
    }

    @action(detail=False, methods=["post"], url_path="imei_check", url_name="imei_check")
    def imei_check(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(is_valid=True, user=request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="generate_imei", url_name="generate_imei")
    def generate_imei(self, request, *args, **kwargs):
        imei = ImeiGenerator().generate()
        serializer = self.get_serializer(data={"imei": imei})
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(is_valid=True, user=request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="user_imei", url_name="user_imei")
    def user_imei(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JwtTokenViewSet(ExtendedListAPIView, ExtendedRetrieveUpdateDestroyAPIView):
    queryset = JwtToken.objects.all()
    permission_by_action = {
        "default": [AllowAny],
    }
    serializers_by_action = {
        "default": JwtTokenEncodeSerializer,
        "decode_jwt_token": JwtTokenDecodeSerializer,
    }

    def get_queryset(self):
        queryset = super(JwtTokenViewSet, self).get_queryset()
        if self.action == "list":
            return queryset.filter(user=self.request.user)
        return queryset

    @action(detail=False, methods=["post"], url_path="encode_jwt_token", url_name="encode_jwt_token")
    def encode_jwt_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt_token = JWTGenerator.encode(validated_data=serializer.validated_data)
        serializer.save(user=request.user if request.user.is_authenticated else None, jwt_token=jwt_token)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="decode_jwt_token", url_name="decode_jwt_token")
    def decode_jwt_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        decoded_data = JWTGenerator.decode(validated_data=serializer.validated_data)
        serializer.save(
            user=request.user if request.user.is_authenticated else None,
            jwt_token=serializer.validated_data["jwt_token"],
            header=decoded_data,
        )
        return Response(serializer.data)
