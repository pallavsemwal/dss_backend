import graphene
from ...models.tasks import Task
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from datetime import date


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class TaskMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        task_data = graphene.JSONString(required=True)

    # The class attributes define the response of the mutation
    task = graphene.Field(TaskType)

    def mutate(self, info, task_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                darr = [int(f) for f in task_data['task_date'].split('-')]
                task = Task(owner=owner,
                            task_name=task_data["task_name"],
                            task_date=date(darr[0], darr[1], darr[2]))
                task.save()
                return TaskMutation(task=task)
            else:
                return None
        except Exception as exception:
            print(exception)
            return None


class DeleteTaskMutation(graphene.Mutation):
    # Arguments
    class Arguments:
        task_id = graphene.ID(required=True)

    # Response
    name = graphene.String()

    # delete Mutation Function
    def mutate(self, info, task_id):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                task = Task.objects.get(owner=owner, id=task_id)
                name = task.task_name
                task.delete()
                return DeleteTaskMutation(name=name)
            else:
                return "User Not Authenticated."
        except Exception as exception:
            return "Error Delete Task Exception"


class Mutation(graphene.ObjectType):
    create_task = TaskMutation.Field()
    delete_task = DeleteTaskMutation.Field()
