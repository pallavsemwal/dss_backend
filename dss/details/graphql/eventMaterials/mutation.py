import graphene
from graphene_file_upload.scalars import Upload
from django.contrib.auth.models import User
from ...models.events import Event
from ...models.eventsMaterials import EventFiles


class EventMaterialMutation(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        notes = graphene.JSONString(required=False)
        files = graphene.List(Upload, required=False)

    success = graphene.Boolean()

    def mutate(self, info, event_id, notes=None, files=None, **kwargs):
        try:
            if info.context.user.is_authenticated:
                user = User.objects.get(username=info.context.user)
                event = Event.objects.get(id=event_id, owner=user)
                if notes is not None:
                    event.mom = notes
                event.save()
                for uploaded_file in files:
                    newfile = EventFiles(file=uploaded_file, event=event)
                    newfile.save()
                return EventMaterialMutation(success=True)
            else:
                return EventMaterialMutation(success=False)
        except Exception as exception:
            print(str(exception))
            return EventMaterialMutation(success=False)


class Mutation(graphene.ObjectType):
    event_material_mutation = EventMaterialMutation.Field()
