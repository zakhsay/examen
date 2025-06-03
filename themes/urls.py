from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
from graphene_django.views import GraphQLView
from .views import AdminThemeViewSet

router = DefaultRouter()
router.register(r'themes', views.AdminThemeViewSet)

urlpatterns = router.urls + [
    path('api/', include(router.urls)),
    path('themes/toggle/', views.AdminThemeViewSet.as_view({'post': 'toggle_active'})),
    path('graphql/', GraphQLView.as_view(graphiql=True)),  # Add this line for GraphQL endpoint
]

