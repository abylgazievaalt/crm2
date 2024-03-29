from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from crmfood import settings
from django.shortcuts import render
from .renderers import UserJSONRenderer
from api.models import *
from api.serializers import *
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    #renderer_classes = (UserJSONRenderer,)
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        serializer = UsersSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user')

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.renderer_classes = JSONRenderer
        
        user_id = request.data.get('user_id', None)
        
        try:
            user = self.queryset.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class UserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UsersSerializer
    
    queryset = User.objects.all()

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    #renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    #renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TableList(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TablesSerializer

class TableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TablesSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

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

class ActiveOrdersList(APIView):
    def get(self, request):
        orders = Order.objects.filter(isitopen=1)
        serializer = OrdersSerializer(orders, many=True)
        
        return Response(serializer.data)
