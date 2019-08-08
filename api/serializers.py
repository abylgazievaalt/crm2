from api.models import *
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'login',
          'password', 'email', 'roleid', 'dateofadd', 'phone']

class TablesSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Table
        fields = ('id', 'name')

class ServicePercentageSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = ServicePercentage
        fields = ('id', 'percentage')

class MealCategoriesSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = MealCategory
        fields = ('name', 'departmentid')

class MealsSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Meal
        fields = ('name', 'categoryid', 'price', 'description')

class RolesSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # users = UsersSerializer(many=True)

    class Meta:
        model = Role
        fields = ('id', 'name')
'''
    def create(self, validated_data):
        users_data = validated_data.pop('users')
        role = Role.objects.create(**validated_data)
        for user in users_data:
            User.objects.create(roleid=role, **user)
        role.save()
        return role
'''

class DepartmentsSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # categories = MealCategoriesSerializer(many=True)

    class Meta:
        model = Department
        fields = ('id', 'name',)
'''
    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        department = Department.objects.create(**validated_data)
        for category in categories_data:
            Category.objects.create(departmentid=department, **category)
        department.save()
        return department
'''
class OrderItemSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), source='meal.id')
    name = serializers.CharField(source='meal.name', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    total = serializers.IntegerField(source='get_total', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'amount', 'price', 'total')

class OrdersSerializer(serializers.ModelSerializer):
    #waiterid = serializers.IntegerField(source='waiter.id', read_only=True)
    #isitopen = serializers.BooleanField(read_only=True, default=True)
    #tableid = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='table.id',)
    tablename = serializers.CharField(source='table.name', read_only=True)
    mealsid = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('tableid', 'tablename', 'isitopen', 'date', 'mealsid')

    def create(self, validated_data):
        meals_data = validated_data.pop('mealsid')
        order = Order.objects.create(isitopen=1, table=validated_data['table']['id'])
        for meal in meals_data:
            OrderItem.objects.create(order=order,**meal)
        order.save()
        return order

class StatusSerializer(serializers.ModelSerializer):

    # order = OrdersSerializer()

    class Meta:
        model = Status
        fields = ('id', 'name')

class MealsToOrderSerializer(serializers.ModelSerializer):

    meals = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('mealsid',)

class ChecksSerializer(serializers.ModelSerializer):

    #orderid = OrdersSerializer()
    meals = MealsToOrderSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('orderid', 'date', 'servicefee', 'totalsum', 'meals')

    def create(self):
        order.isitopen = False
        order.save()
        checks = Check.objects.create(order=order, percentage = ServicePercentage.objects.all()[0], **validated_data)
        checks.save()
        return checks
