import graphene
from graphene_django.types import DjangoObjectType
from ...models.schemes import Scheme
from django.db.models import Sum
from django.contrib.auth.models import User
import json


class SchemeType(DjangoObjectType):
    class Meta:
        model = Scheme


class Query(object):
    scheme = graphene.Field(SchemeType, id=graphene.ID(), name=graphene.String(), district_name=graphene.String())
    all_schemes = graphene.List(graphene.JSONString)
    top_schemes = graphene.List(SchemeType)
    all_schemes_district = graphene.List(SchemeType)

    def resolve_all_schemes(self, info, **kwargs):
        data = list(map(json.dumps,
                        Scheme.objects.values('name')
                        .annotate(num_people_reached=Sum('num_people_reached'),
                                  num_people_left=Sum('num_people_left'))))
        return data


    def resolve_scheme(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        district_name = kwargs.get('district_name')

        if id is not None:
            return Scheme.objects.get(pk=id, district__name=district_name)

        if name is not None:
            return Scheme.objects.get(name=name, district__name=district_name)

        return None

    def resolve_top_schemes(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            for district in user.profile.district.all():
                return Scheme.objects.filter(district=district).order_by('-num_people_reached')[:3]


    def resolve_all_schemes_district(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            for district in user.profile.district.all():
                return Scheme.objects.filter(district=district)

