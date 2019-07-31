from .models import *
from .serializers import *
from rest_framework import generics, viewsets
from django.shortcuts import render

class TablesView(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class MealCategoriesView(viewsets.ModelViewSet):
    queryset = MealCategory.objects.all()
    serializer_class = MealCategorySerializer

class DepartmentsView(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class StatusView(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ServicePercentageView(viewsets.ModelViewSet):
    queryset = ServicePercentage.objects.all()
    serializer_class = ServicePercentageSerializer

class OrdersPercentageView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class MealsView(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class RolesView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ChecksView(viewsets.ModelViewSet):
    queryset = ServicePercentage.objects.all()
    serializer_class = CheckSerializer
