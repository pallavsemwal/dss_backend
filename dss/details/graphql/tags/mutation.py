import graphene
from ...models.tags import Tag
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class TagMutation(graphene.Mutation):
    class Arguments:
        tag_data = graphene.JSONString(required=True)

    tag = graphene.Field(TagType)

    def mutate(self, info, tag_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                tag = Tag(owner=owner,
                          name=tag_data['tag_name'],
                        #   details=tag_data['tag_details']
                          )
                tag.save()
                return TagMutation(tag=tag)
            else:
                return None
        except Exception as exception:
            return None

class UpdateTagMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        tag_data = graphene.JSONString(required=True)

    tag = graphene.Field(TagType)

    def mutate(self, info, id, tag_data):
        try:
            if info.context.user.is_authenticated:
                
                tag = Tag.objects.get(pk= id)
                
                tag.name = tag_data['tag_name']
                tag.details = tag_data['tag_details']
                tag.save()

                return UpdateTagMutation(tag=tag)
            else:
                return None
        except Exception as exception:
            return None

class DeleteTagMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)

    name = graphene.String()

    def mutate(self, info, id):
        try:
            if info.context.user.is_authenticated:
                tag = Tag.objects.get(pk= id)
                name = tag.name
                tag.delete()

                return DeleteTagMutation(name = name)
            else:
                return None
        except Exception as exception:
            return None

class Mutation(graphene.ObjectType):
    create_tag = TagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()