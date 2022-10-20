import graphene
from ...models.events import Event
from .types import EventType
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
import datetime
import pytz


class Query(object):
    events_duration_exclude_all_day = graphene.List(
        EventType, starttime=graphene.String(), endtime=graphene.String())
    events_duration_all_day = graphene.List(
        EventType, starttime=graphene.String(), endtime=graphene.String())
    all_events = graphene.List(EventType)
    events_upcoming = graphene.List(EventType, curtime=graphene.String())
    search_events = graphene.List(
        EventType, event_data=graphene.JSONString(required=True))
    suggest_events = graphene.List(EventType, start_string=graphene.String())

    def resolve_all_events(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Event.objects.filter(owner=user)

    def resolve_events_duration_exclude_all_day(self, info, **kwargs):
        if info.context.user.is_authenticated:
            start_dur = datetime.datetime.strptime(kwargs.get('starttime'), '%Y-%m-%dT%H:%M:%SZ').replace(
                tzinfo=pytz.utc)
            end_dur = datetime.datetime.strptime(kwargs.get(
                'endtime'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            user = User.objects.get(username=info.context.user)
            return Event.objects.filter(owner=user, is_all_day=False, end_date_time__gt=start_dur,
                                        start_date_time__lt=end_dur)

    def resolve_events_duration_all_day(self, info, **kwargs):
        if info.context.user.is_authenticated:
            start_dur = datetime.datetime.strptime(kwargs.get('starttime'), '%Y-%m-%dT%H:%M:%SZ').replace(
                tzinfo=pytz.utc)
            end_dur = datetime.datetime.strptime(kwargs.get(
                'endtime'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            user = User.objects.get(username=info.context.user)
            return Event.objects.filter(owner=user, is_all_day=True, end_date_time__gte=start_dur,
                                        start_date_time__lte=end_dur)

    def resolve_events_upcoming(self, info, **kwargs):
        if info.context.user.is_authenticated:
            curr_time = datetime.datetime.strptime(kwargs.get(
                'curtime'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            user = User.objects.get(username=info.context.user)
            return Event.objects.filter(owner=user, is_all_day=False, start_date_time__gte=curr_time).order_by(
                'start_date_time')[:5]

    def resolve_search_events(self, info, event_data):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            filtered_events = Event.objects.filter(owner=user)
            basic_filters = Q()
            if event_data["is_basic_search"]:
                vector = SearchVector("event_name", "location", "mom")
                query = SearchQuery(event_data["content"])
                words = event_data["content"].split()
                for word in words:
                    basic_filters = basic_filters | Q(
                        event_name__icontains=word)
                    basic_filters = basic_filters | Q(location__icontains=word)
                return filtered_events.annotate(rank=SearchRank(vector, query)).order_by('-rank').filter(basic_filters)[:10]
            else:
                search_params = event_data.keys()
                filters = Q()
                if "priority" in search_params:
                    filters = filters & Q(priority=int(event_data["priority"]))
                if "event_name" in search_params:
                    words = event_data["event_name"].split()
                    for word in words:
                        filters = filters & Q(event_name__icontains=word)
                if "location" in search_params:
                    words = event_data["location"].split()
                    for word in words:
                        filters = filters & Q(location__icontains=word)
                if "start_date" in search_params:
                    start_date_time = datetime.datetime.strptime(
                        event_data['start_date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                    filters = filters & Q(start_date_time__gt=start_date_time)
                if "end_date" in search_params:
                    end_date_time = datetime.datetime.strptime(
                        event_data['end_date'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                    filters = filters & Q(end_date_time__lt=end_date_time)
                if "tags" in search_params:
                    for tag in event_data["tags"]:
                        filters = filters & Q(tags__id=tag)
                if event_data["is_all_day"]:
                    filters = filters & Q(is_all_day=True)
                print(filters)
                return filtered_events.filter(filters)

    def resolve_suggest_events(self, info, start_string):
        if info.context.user.is_authenticated:
            user = User.objects.get(username=info.context.user)
            return Event.objects.filter(owner=user, is_all_day=False, event_name__icontains=start_string)[:10]
