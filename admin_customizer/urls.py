from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('themes.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
