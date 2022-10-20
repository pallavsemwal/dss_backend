import graphene
from graphene_django.types import DjangoObjectType
from ...models.district import District


class DistrictType(DjangoObjectType):
    class Meta:
        model = District


class Query(object):
    district = graphene.Field(DistrictType, id=graphene.ID(), name=graphene.String())
    all_districts = graphene.List(DistrictType)

    def resolve_all_districts(self, info, **kwargs):
        return District.objects.all()

    def resolve_district(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return District.objects.get(pk=id)

        if name is not None:
            return District.objects.get(name=name)

        return None