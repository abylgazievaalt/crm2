from django.urls import path, include
from rest_framework import routers
from api import views

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
#router.register(r'api', views.CourseView)

router.register(r'tables', views.TablesView)
router.register(r'categories', views.CategoriesView)

# The API URLs are now determined automatically by the router.
urlpatterns = [
               path('', include(router.urls))
]

