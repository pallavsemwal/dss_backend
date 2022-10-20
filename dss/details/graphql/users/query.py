import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from ...models.profile import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class Query(object):
    user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return User.objects.get(username=info.context.user)

        return None
