import graphene
import app_graph.schema
import graphql_jwt


class Query(app_graph.schema.Query,graphene.ObjectType):
    pass


class Mutation(app_graph.schema.Mutation,graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field() ######https://www.howtographql.com/graphql-python/4-authentication/

schema=graphene.Schema(query=Query,mutation=Mutation)










