import graphene
from graphene_django import DjangoObjectType
from graphene_django.views import GraphQLView
from themes.models import AdminTheme
from themes.serializers import AdminThemeSerializer

class AdminThemeType(DjangoObjectType):
    class Meta:
        model = AdminTheme
        fields = '__all__'

class Query(graphene.ObjectType):
    themes = graphene.List(AdminThemeType)
    active_theme = graphene.Field(AdminThemeType)

    def resolve_themes(self, info):
        return AdminTheme.objects.all()

    def resolve_active_theme(self, info):
        return AdminTheme.objects.filter(is_active=True).first()

class ToggleTheme(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    theme = graphene.Field(AdminThemeType)

    def mutate(self, info, id):
        theme = AdminTheme.objects.get(pk=id)
        theme.is_active = True
        theme.save()
        return ToggleTheme(theme=theme)

class CreateTheme(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        css_url = graphene.String(required=True)
        js_url = graphene.String(required=True)
        is_active = graphene.Boolean(required=True)

    theme = graphene.Field(AdminThemeType)

    def mutate(self, info, name, css_url, js_url, is_active):
        theme = AdminTheme.objects.create(
            name=name,
            css_url=css_url,
            js_url=js_url,
            is_active=is_active
        )
        return CreateTheme(theme=theme)

class Mutation(graphene.ObjectType):
    toggle_theme = ToggleTheme.Field()
    create_theme = CreateTheme.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)