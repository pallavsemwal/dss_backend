import graphene
from ...models.tags import Tag
from .mutation import TagType
from django.contrib.auth.models import User


class Query(object):
    all_tags = graphene.List(TagType)

    def resolve_all_tags(self, info, **kwargs):
        print("Resolving All Tags")
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Tag.objects.filter(owner=user)
