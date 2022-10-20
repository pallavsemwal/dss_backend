import graphene
from ...models.schemes import Scheme
from ...models.district import District

class SchemeMutation(graphene.Mutation):
    class Arguments:
        scheme_data = graphene.JSONString(required = True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, scheme_data):
        try:
            district = District.objects.get(name=scheme_data["district"])
            schemes = Scheme(
                        name = scheme_data["name"],
                        district = district,
                        details = scheme_data["details"],
                        num_people_reached = scheme_data["num_people_reached"],
                        num_people_left = scheme_data["num_people_left"]
                        )
            schemes.save()
            print(schemes)
            return SchemeMutation(success=True, message= "succesfully added the Scheme!")
        except Exception as exception:
            print(exception)
            return SchemeMutation(success=False, message="Sorry, some error occured!!")

class Mutation(graphene.ObjectType):
    create_scheme = SchemeMutation.Field()
