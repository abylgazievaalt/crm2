from django.urls import path, include
from rest_framework import routers
from api import views
#from rest_framework.schemas import get_schema_view

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
#router.register(r'api', views.CourseView)
router.register(r'categories', views.CategoryView)
router.register(r'tables', views.TableView)
#schema_view = get_schema_view(title='Pastebin API')

# The API URLs are now determined automatically by the router.
urlpatterns = [
               #path('schema/', schema_view),
               path('', include(router.urls)),
               ]

