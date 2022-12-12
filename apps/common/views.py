from rest_framework.viewsets import GenericViewSet

DEFAULT = 'default'


class CustomGenericViewSet(GenericViewSet):
    serializers_by_action = {}
    permission_by_action = {}
    authentication_by_action = {}


def get_serializer_class(self):
    if serializer := self.serializers_by_action.get(self.action) or self.serializers_by_action.get(DEFAULT):
        return serializer
    return super(CustomGenericViewSet, self).get_serializer_class()


def get_permissions(self):
    if self.action in self.permission_by_action or DEFAULT in self.permission_by_action:
        return [permission() for permission in self.permission_by_action[self.action]]


def get_authenticators(self):
    if self.action in self.authentication_by_action or DEFAULT in self.authentication_by_action:
        return [authenticator() for authenticator in self.authentication_by_action[self.action]]
