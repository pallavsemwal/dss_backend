import graphene
from ...models.events import Event
from django.contrib.auth.models import User
from .utils import check_if_can_be_added, check_if_can_be_updated
import datetime
from .types import EventType
import pytz
from ..constants import StatusCodes


class EventMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        event_data = graphene.JSONString(required=True)

    # The class attributes define the response of the mutation
    statusCode = graphene.String()
    message = graphene.String()
    eventdata = graphene.JSONString()

    def mutate(self, info, event_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                start_date_time = datetime.datetime.strptime(event_data["start_date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)
                end_date_time = datetime.datetime.strptime(event_data["end_date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)
                can_be_added, info_message = check_if_can_be_added(owner, start_date_time, end_date_time,
                                                                   event_data["venue"],
                                                                   int(event_data["priority"]),
                                                                   event_data["is_all_day"])
                if can_be_added:
                    event = Event(owner=owner,
                                  event_name=event_data["event_name"],
                                  is_all_day=event_data["is_all_day"],
                                  start_date_time=start_date_time,
                                  location=event_data["venue"],
                                  end_date_time=end_date_time,
                                  priority=int(event_data["priority"]))
                    event.save()
                    event.tags.set(event_data['tags'])
                    return EventMutation(statusCode=StatusCodes.SUCCESS, message=info_message)
                else:
                    return EventMutation(statusCode=StatusCodes.FORBIDDEN, message=info_message, eventdata=event_data)
            else:
                return EventMutation(statusCode=StatusCodes.UNAUTHORIZED, message="Unauthenticated User")
        except Exception as exception:
            return EventMutation(statusCode=StatusCodes.INTERNAL_SERVER_ERROR, message="Unsuccessful: Try Again!")


class ForceEventMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        event_data = graphene.JSONString(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()
    message = graphene.String()
    event = graphene.Field(EventType)

    def mutate(self, info, event_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                start_date_time = datetime.datetime.strptime(event_data["start_date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)
                end_date_time = datetime.datetime.strptime(event_data["end_date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)

                event = Event(owner=owner,
                              event_name=event_data["event_name"],
                              is_all_day=event_data["is_all_day"],
                              start_date_time=start_date_time,
                              location=event_data["venue"],
                              end_date_time=end_date_time,
                              priority=int(event_data["priority"]))
                event.save()
                event.tags.set(event_data['tags'])
                return ForceEventMutation(success=True, message="The Event has been added succesfully", event=event)
            else:
                return ForceEventMutation(success=False, message="Unauthenticated User")
        except Exception as exception:
            return ForceEventMutation(success=False, message="Unsuccessful: Try Again!")


class DeleteEventMutation(graphene.Mutation):
    # Arguments
    class Arguments:
        event_id = graphene.ID(required=True)

    # Response
    name = graphene.String()

    # delete Mutation Function
    def mutate(self, info, event_id):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                event = Event.objects.get(owner=owner, id=event_id)
                name = event.event_name
                event.delete()
                return DeleteEventMutation(name=name)
            else:
                return "User Not Authenticated."
        except Exception as exception:
            return "Error Delete Event Exception"


class UpdateEventMutation(graphene.Mutation):
    class Arguments:
        event_data = graphene.JSONString(required=True)

    statusCode = graphene.String()
    message = graphene.String()
    event = graphene.Field(EventType)
    eventdata = graphene.JSONString()

    def mutate(self, info, event_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                event = Event.objects.get(owner=owner, id=event_data['id'])
                start_date_time = datetime.datetime.strptime(event_data["starttime"],
                                                             '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                end_date_time = datetime.datetime.strptime(event_data["endtime"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)
                can_be_updated, info_message = check_if_can_be_updated(
                    owner, event, start_date_time, end_date_time, event.priority)
                if can_be_updated:
                    event.start_date_time = start_date_time
                    event.end_date_time = end_date_time
                    event.save()
                    return UpdateEventMutation(statusCode=StatusCodes.SUCCESS, message=info_message, event=event)
                else:
                    return UpdateEventMutation(statusCode=StatusCodes.FORBIDDEN, message=info_message, eventdata=event_data)
            else:
                return UpdateEventMutation(statusCode=StatusCodes.UNAUTHORIZED, message="Unauthenticated User")
        except Exception as exception:
            return UpdateEventMutation(statusCode=StatusCodes.INTERNAL_SERVER_ERROR, message="Unsuccessful! Try Again!")


class ForceUpdateEventMutation(graphene.Mutation):
    class Arguments:
        event_data = graphene.JSONString(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    event = graphene.Field(EventType)

    def mutate(self, info, event_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                event = Event.objects.get(owner=owner, id=event_data['id'])
                start_date_time = datetime.datetime.strptime(
                    event_data["starttime"], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                end_date_time = datetime.datetime.strptime(
                    event_data["endtime"], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                can_be_updated, info_message = check_if_can_be_updated(
                    owner, event, start_date_time, end_date_time, event.priority)

                event.start_date_time = start_date_time
                event.end_date_time = end_date_time
                event.save()
                return ForceUpdateEventMutation(success=True, message=info_message, event=event)

            else:
                return ForceUpdateEventMutation(success=False, message="Unauthenticated User")
        except Exception as exception:
            return ForceUpdateEventMutation(success=False, message="Unsuccessful! Try Again!")


class CompleteUpdateEventMutation(graphene.Mutation):
    """ Mutation is used when complete update of the event is required. """
    class Arguments:
        event_data = graphene.JSONString(required=True)

    statusCode = graphene.String()
    message = graphene.String()
    eventdata = graphene.JSONString()

    def mutate(self, info, event_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                event = Event.objects.get(owner=owner, id=event_data['id'])
                start_date_time = datetime.datetime.strptime(event_data["start_date"],
                                                             '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                end_date_time = datetime.datetime.strptime(event_data["end_date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)
                can_be_updated, info_message = check_if_can_be_updated(
                    owner, event, start_date_time, end_date_time, int(event_data["priority"]))
                if can_be_updated:
                    event.start_date_time = start_date_time
                    event.end_date_time = end_date_time
                    event.priority = int(event_data["priority"])
                    event.event_name = event_data["event_name"]
                    event.is_all_day = event_data["is_all_day"]
                    event.location = event_data["venue"]
                    event.save()
                    event.tags.set(event_data["tags"])
                    return CompleteUpdateEventMutation(statusCode=StatusCodes.SUCCESS, message=info_message)
                else:
                    return CompleteUpdateEventMutation(statusCode=StatusCodes.FORBIDDEN, message=info_message, eventdata=event_data)
            else:
                return CompleteUpdateEventMutation(statusCode=StatusCodes.UNAUTHORIZED, message="Unauthenticated User")
        except Exception as exception:
            print(exception)
            return CompleteUpdateEventMutation(statusCode=StatusCodes.INTERNAL_SERVER_ERROR, message="Unsuccessful! Try Again!")


class ForceCompleteUpdateEventMutation(graphene.Mutation):
    class Arguments:
        event_data = graphene.JSONString(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, event_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                event = Event.objects.get(owner=owner, id=event_data['id'])
                start_date_time = datetime.datetime.strptime(event_data["start_date"],
                                                             '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                end_date_time = datetime.datetime.strptime(event_data["end_date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)

                event.start_date_time = start_date_time
                event.end_date_time = end_date_time
                event.priority = int(event_data["priority"])
                event.event_name = event_data["event_name"]
                event.is_all_day = event_data["is_all_day"]
                event.location = event_data["venue"]
                event.save()
                event.tags.set(event_data["tags"])
                return ForceCompleteUpdateEventMutation(success=True, message="Event Updated Succesfully")
            else:
                return ForceCompleteUpdateEventMutation(success=False, message="Unauthenticated User")
        except Exception as exception:
            print(exception)
            return ForceCompleteUpdateEventMutation(success=False, message="Unsuccessful! Try Again!")


class Mutation(graphene.ObjectType):
    create_event = EventMutation.Field()
    force_create_event = ForceEventMutation.Field()
    delete_event = DeleteEventMutation.Field()
    update_event = UpdateEventMutation.Field()
    force_update_event = ForceUpdateEventMutation.Field()
    complete_update_event = CompleteUpdateEventMutation.Field()
    force_complete_update_event = ForceCompleteUpdateEventMutation.Field()
