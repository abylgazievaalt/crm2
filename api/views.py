from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from crmfood import settings
from django.shortcuts import render

from api.models import *
from api.serializers import *
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.signals import user_logged_in


class TableList(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TablesSerializer

class TableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TablesSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = MealCategory.objects.all()
    serializer_class = MealCategoriesSerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MealCategory.objects.all()
    serializer_class = MealCategoriesSerializer

class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RolesSerializer

class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RolesSerializer

class MealList(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealsSerializer

class MealDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealsSerializer

class MealToOrderList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = MealsToOrderSerializer

class MealsToOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = MealsToOrderSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer

class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentsSerializer

class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentsSerializer

class StatusList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ServicePercentageList(generics.ListCreateAPIView):
    queryset = ServicePercentage.objects.all()
    serializer_class = ServicePercentageSerializer

class ServicePercentageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServicePercentage.objects.all()
    serializer_class = ServicePercentageSerializer

class CheckList(generics.ListCreateAPIView):
    queryset = Check.objects.all()
    serializer_class = ChecksSerializer

class CheckDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Check.objects.all()
    serializer_class = ChecksSerializer
