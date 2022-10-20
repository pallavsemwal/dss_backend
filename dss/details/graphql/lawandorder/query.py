import graphene
from .types import RallyType, EpidemicType, CalamityType, CrimeType, GatheringType
from ...models.crime import Crime
from ...models.calamity import Calamity
from ...models.epidemic import Epidemic
from ...models.rally import Rally
from ...models.publicGathering import PublicGathering
from django.contrib.auth.models import User


class Query(object):
    all_crimes = graphene.List(CrimeType)
    all_rallies = graphene.List(RallyType)
    all_epidemics = graphene.List(EpidemicType)
    all_calamities = graphene.List(CalamityType)
    all_gatherings = graphene.List(GatheringType)

    def resolve_all_crimes(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Crime.objects.filter(owner=user).order_by('-date_time')

    def resolve_all_calamities(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Calamity.objects.filter(owner=user).order_by('-start_date')

    def resolve_all_epidemics(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Epidemic.objects.filter(owner=user).order_by('-year')

    def resolve_all_rallies(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Rally.objects.filter(owner=user).order_by('-date')


    def resolve_all_gatherings(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return PublicGathering.objects.filter(owner=user).order_by('-date')

    
