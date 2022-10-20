from ...models.events import Event
from ...models.eventsMaterials import EventFiles
from graphene_django.types import DjangoObjectType


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class EventFilesType(DjangoObjectType):
    class Meta:
        model = EventFiles
