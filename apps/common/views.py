from django_filters import FilterSet
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.viewsets import GenericViewSet

DEFAULT = "default"


class ExtendedViewSet(GenericViewSet):
    serializers_by_action = {}
    permission_by_action = {}

    def get_serializer_class(self):
        if serializer := self.serializers_by_action.get(self.action) or self.serializers_by_action.get(DEFAULT):
            return serializer
        return super(ExtendedViewSet, self).get_serializer_class()

    def get_permissions(self):
        if self.action in self.permission_by_action or "default" in self.permission_by_action:
            try:
                return [permission() for permission in self.permission_by_action[self.action]]
            except KeyError:
                return [permission() for permission in self.permission_by_action[DEFAULT]]
        return super().get_permissions()


class ExtendedListAPIView(ListAPIView, ExtendedViewSet):
    def __init__(self, **kwargs):
        if not hasattr(self, "filter_class") and hasattr(self, "filterset_fields"):
            # Dynamic filter classes
            namespace = self.queryset.model.__name__
            self.filter_class = type(
                f"{namespace}FilterClass",
                (FilterSet,),
                {
                    "Meta": type(
                        f"{namespace}FilterMetaClass",
                        (object,),
                        {"model": self.queryset.model, "fields": self.filterset_fields},
                    )
                },
            )

        super().__init__(**kwargs)


class ExtendedCreateAPIView(CreateAPIView, ExtendedViewSet):
    ...


class ExtendedRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView, ExtendedViewSet
):
    ...


class ExtendedRetrieveAPIView(RetrieveAPIView, ExtendedViewSet):
    ...


class BasicModelViewSet(
    ExtendedListAPIView,
    ExtendedCreateAPIView,
    ExtendedRetrieveUpdateDestroyAPIView,
    ExtendedViewSet,
):
    ...
