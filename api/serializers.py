from api.models import *
from rest_framework import serializers

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    
    #id = serializers.IntegerField(required=False)
    waiters
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'login',
                  'password', 'email', 'roleid', 'dateofadd', 'phone']

class RoleSerializer(serializers.ModelSerializer):
    
    users = UserSerializer(many=True)

    class Meta:
        model = Role
        fields = ('id', 'name')

    def create(self, validated_data):
        users_data = validated_data.pop('users')
        role = Role.objects.create(**validated_data)
        for user in users_data:
            User.objects.create(roleid=role, **user)
        role.save()
        return role

class DepartmentSerializer(serializers.ModelSerializer):
    
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Department
        fields = ('id', 'name')

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        department = Department.objects.create(**validated_data)
        for category in categories_data:
            Category.objects.create(departmentid=department, **category)
        department.save()
        return department

class CategorySerializer(serializers.ModelSerializer):

    meals = MealSerializer(many=True)
    
    class Meta:
        model = Category
        fields = ('name', 'departmentid')

    def create(self, validated_data):
        meals_data = validated_data.pop('meals')
        category = Category.objects.create(**validated_data)
        for meal in meals_data:
            Meal.objects.create(categoryid=category, **meal)
        category.save()
        return category

class StatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Status
        fields = ('id', 'name')

class ServicePercentageSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = ServicePercentage
        fields = ('id', 'percentage')

class MealSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Meal
        fields = ('name', 'categoryid', 'price', 'description', 'mealstoorder')

class OrderSerializer(serializers.ModelSerializer):
    
    waiter = Role.objects.get(name='waiter')
    waiterid = waiter.id
    check = CheckSerializer(many=False)
    mealstoorder = MealToOrderSerializer(many = True)
    
    class Meta:
        model = Order
        fields = ('waiterid', 'tableid', 'isitopen', 'date')

    def create(self, validated_data):
        check_data = validated_data.pop('check')
        mealstoorder_data = validated_data.pop('mealstoorder')
        order = Order.objects.create(**validated_data)
        for meal in mealstoorder_data:
            MealToOrder.objects.create(orderid=order, **meal)
        Check.objects.create(orderid=order, **check_data)
        order.save()
        return order

class CheckSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ('orderid', 'date', 'servicefee', 'totalsum')

class MealToOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = MealToOrder
        fields = ('uniqueid', 'orderid')
