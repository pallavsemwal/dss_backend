import graphene
from ...models.tasks import Task
from .mutation import TaskType
from django.contrib.auth.models import User
import datetime
import pytz

class Query(object):
    all_tasks = graphene.List(TaskType)
    tasks_duration = graphene.List(TaskType, starttime=graphene.String(), endtime=graphene.String())

    def resolve_all_tasks(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Task.objects.filter(owner=user)

    def resolve_tasks_duration(self, info, **kwargs):
        if info.context.user.is_authenticated:
            start_dur = [int(f) for f in kwargs.get('starttime').split('-')]
            end_dur = [int(f) for f in kwargs.get('endtime').split('-')]
            start_dur = datetime.date(start_dur[0], start_dur[1], start_dur[2])
            end_dur = datetime.date(end_dur[0], end_dur[1], end_dur[2])
            user = User.objects.get(username=info.context.user)
            return Task.objects.filter(owner=user, task_date__gte=start_dur, task_date__lte=end_dur)
