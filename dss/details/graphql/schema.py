import graphene
from .schemes.query import Query as SchemeQuery
from .district.query import Query as DistrictQuery
from .users.query import Query as UserQuery
from .events.query import Query as EventQuery
from .tasks.query import Query as TaskQuery
from .tags.query import Query as TagQuery
from .lawandorder.query import Query as LawAndOrderQuery

from .events.mutation import Mutation as EventMutation
from .tasks.mutation import Mutation as TaskMutation
from .tags.mutation import Mutation as TagMutation
from .eventMaterials.mutation import Mutation as EventMaterialMutation
from .lawandorder.mutation import Mutation as LawAndOrderMutation
from .schemes.mutation import Mutation as SchemesMutation


class Queries(TagQuery, SchemeQuery, DistrictQuery, UserQuery, EventQuery, TaskQuery, LawAndOrderQuery,
              graphene.ObjectType):
    pass


class Mutations(TagMutation, TaskMutation, EventMutation, EventMaterialMutation, LawAndOrderMutation, SchemesMutation,
                graphene.ObjectType):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)
