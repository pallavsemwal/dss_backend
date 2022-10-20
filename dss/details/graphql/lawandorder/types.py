from ...models.lawAndOrder import LawAndOrder
from ...models.crime import Crime
from ...models.calamity import Calamity
from ...models.epidemic import Epidemic
from ...models.rally import Rally
from ...models.publicGathering import PublicGathering
from graphene_django.types import DjangoObjectType


class LawAndOrderType(DjangoObjectType):
    class Meta:
        model = LawAndOrder

class GatheringType(DjangoObjectType):
    class Meta:
        model = PublicGathering

class RallyType(DjangoObjectType):
    class Meta:
        model = Rally

class CrimeType(DjangoObjectType):
    class Meta:
        model = Crime

class EpidemicType(DjangoObjectType):
    class Meta:
        model = Epidemic

class CalamityType(DjangoObjectType):
    class Meta:
        model = Calamity