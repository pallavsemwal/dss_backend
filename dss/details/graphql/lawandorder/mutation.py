import graphene
from ...models.lawAndOrder import LawAndOrder
from ...models.rally import Rally
from ...models.calamity import Calamity
from ...models.crime import Crime
from ...models.epidemic import Epidemic
from ...models.publicGathering import PublicGathering
from django.contrib.auth.models import User
import datetime
import pytz


class RallyMutation(graphene.Mutation):
    class Arguments:
        rally_data = graphene.JSONString(required = True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, rally_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                date = datetime.datetime.strptime(rally_data["date"], '%d-%m-%Y').date()
                rally = Rally(owner= owner, 
                            rally_title= rally_data["title"], 
                            religious=rally_data["is_religious"], 
                            political = rally_data["is_political"], 
                            social= rally_data["is_social"], 
                            protest= rally_data["is_protest"], 
                            government=rally_data["is_government"], 
                            attendance=rally_data["attendance"], 
                            police  =rally_data["police"],
                            ambulance = rally_data["ambulance"],
                            firefighters = rally_data["firefighter"],
                            end_location = rally_data["end_location"],
                            start_location = rally_data["start_location"],
                            stationary = rally_data["is_stationary"],
                            lessons_learnt = rally_data["lessons_learnt"],
                            date = date )
                print(rally.lessons_learnt)
                rally.save()
                return RallyMutation(success=True, message= "succesfully added the Rally!")
            else:
                return RallyMutation(success=False, message="Unauthenticated User!!")
        except Exception as exception:
            print(exception)
            return RallyMutation(success=False, message="Sorry, some error occured!!")

class GatheringMutation(graphene.Mutation):
    class Arguments:
        gathering_data = graphene.JSONString(required = True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, gathering_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                date = datetime.datetime.strptime(gathering_data["date"], '%d-%m-%Y').date()
                gathering = PublicGathering(owner= owner, 
                            title= gathering_data["title"], 
                            religious=gathering_data["is_religious"], 
                            political = gathering_data["is_political"], 
                            social= gathering_data["is_social"], 
                            protest= gathering_data["is_protest"], 
                            government=gathering_data["is_government"], 
                            attendance=gathering_data["attendance"], 
                            police  =gathering_data["police"],
                            ambulance = gathering_data["ambulance"],
                            firefighters = gathering_data["firefighter"],
                            location = gathering_data["location"],
                            close = gathering_data["is_close"],
                            duration = gathering_data["duration"],
                            lessons_learnt = gathering_data["lessons_learnt"],
                            date = date )
                print(gathering.lessons_learnt)
                gathering.save()
                return GatheringMutation(success=True, message= "succesfully added the Rally!")
            else:
                return GatheringMutation(success=False, message="Unauthenticated User!!")
        except Exception as exception:
            print(exception)
            return GatheringMutation(success=False, message="Sorry, some error occured!!")


class CalamityMutation(graphene.Mutation):
    class Arguments:
        calamity_data = graphene.JSONString(required = True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, calamity_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                start_date = datetime.datetime.strptime(calamity_data["start_date"], '%d-%m-%Y').date()
                end_date = datetime.datetime.strptime(calamity_data["end_date"], '%d-%m-%Y').date()
                calamity = Calamity(owner= owner,
                                    calamity_type=calamity_data["type"],
                                    title = calamity_data["title"],
                                    total_cost= calamity_data["total_cost"],
                                    injured= calamity_data["injured"],
                                    dead= calamity_data["dead"],
                                    people_affected = calamity_data["people_affected"],
                                    police = calamity_data["police"],
                                    ambulance = calamity_data["ambulance"],
                                    ndrf = calamity_data["ndrf"],
                                    lesson_learnt = calamity_data["lessons_learnt"],
                                    start_date= start_date,
                                    end_date= end_date,)
                print(calamity.lesson_learnt)                   
                calamity.save()
                return CalamityMutation(success=True, message="succesfully added the Calamity")
            else:
                return CalamityMutation(success=False, message="Unauthenticated User!!")
        except Exception as exception:
            print(exception)
            return CalamityMutation(success=False, message="Sorry, some error occured!!")

class CrimeMutation(graphene.Mutation):
    class Arguments:
        crime_data = graphene.JSONString(required = True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, crime_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                date_time = datetime.datetime.strptime(crime_data["date"], '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=pytz.utc)
                crime = Crime(owner= owner,
                                title = crime_data["title"],
                                crime_type=crime_data["crime_type"],
                                area= crime_data["area"],
                                lesson_learnt = crime_data["lessons_learnt"],
                                date_time=date_time)
                print(crime.lesson_learnt)
                crime.save()    
                return CrimeMutation(success=True, message="succesfully added the Crime")
            else:
                return CrimeMutation(success=False, message="Unauthenticated User!!")
        except Exception as exception:
            print(exception)
            return CrimeMutation(success=False, message="Sorry, some error occured!!")
                
class EpidemicMutation(graphene.Mutation):
    class Arguments:
        epidemic_data = graphene.JSONString(required = True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, epidemic_data):
        try:
            if info.context.user.is_authenticated:
                owner = User.objects.get(username=info.context.user)
                date = datetime.datetime.strptime(epidemic_data["year"], '%d-%m-%Y').date()
                epidemic = Epidemic(owner= owner,
                                    title= epidemic_data["title"],
                                    epidemic_type= epidemic_data["type"],
                                    total_infected= epidemic_data["total_infected"],
                                    cured= epidemic_data["cured"],
                                    died= epidemic_data["died"],
                                    police= epidemic_data["police"],
                                    hospitalbeds = epidemic_data["hospitalbeds"],
                                    healthstaff = epidemic_data["healthstaff"],
                                    lesson_learnt = epidemic_data["lessons_learnt"],
                                    date = date)
                print(epidemic.lesson_learnt)
                epidemic.save()
                                
                return EpidemicMutation(success=True, message="succesfully added the epidemic")
            else:
                return EpidemicMutation(success=False, message="Unauthenticated User!!")
        except Exception as exception:
            return EpidemicMutation(success=False, message="Sorry, some error occured!!")
                


class LawAndOrderMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        situation_type = graphene.String(required=True)
        configuration = graphene.JSONString(required=True)
        arrangements = graphene.JSONString(required=True)

    # The class attributes define the response of the mutation
    success = graphene.Boolean()

    def mutate(self, info, situation_type, configuration, arrangements):
        try:
            if info.context.user.is_authenticated:
                situation = LawAndOrder(situation_type=situation_type,
                                        configuration=configuration,
                                        arrangements=arrangements)
                situation.save()
                return LawAndOrderMutation(success=True)
            else:
                return LawAndOrderMutation(success=False)
        except Exception as exception:
            return LawAndOrderMutation(success=False)


class Mutation(graphene.ObjectType):
    create_law_and_order_situation = LawAndOrderMutation.Field()
    create_rally = RallyMutation.Field()
    create_crime = CrimeMutation.Field()
    create_epidemic = EpidemicMutation.Field()
    create_calamity = CalamityMutation.Field()
    create_gathering = GatheringMutation.Field()
    
