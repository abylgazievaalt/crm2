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

class StatusSerializer(serializers.ModelSerializer):
    
    # order = OrdersSerializer()
    
    class Meta:
        model = Status
        fields = ('id', 'name')

class CategoriesSerializer(serializers.ModelSerializer):
    #serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ('name', 'department')

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

class DepartmentsSerializer(serializers.ModelSerializer):
    serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name',)

class OrderItemSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), source='meal.id')
    name = serializers.CharField(source='meal.name', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    total = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'count', 'price', 'total')

class OrdersSerializer(serializers.ModelSerializer):
    waiterid = serializers.IntegerField(source='waiter.id', read_only=True)
    tableid = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='table.id',)
    tablename = serializers.CharField(source='table.name', read_only=True)
    mealsid = OrderItemSerializer(many=True, required=False)
    
    class Meta:
        model = Order
        fields = ('id','waiterid', 'tableid',
                      'tablename', 'isitopen', 'date', 'mealsid')

    def create(self, validated_data):
        order = Order.objects.create(isitopen=1,table=validated_data['table']['id'])
            
        for meal in validated_data['mealsid']:
            OrderItem.objects.create(order=order, meal=meal['meal']['id'], count=meal['count'] ).save()
        
        order.save()
        return order

class MealsToOrderSerializer(serializers.ModelSerializer):
    
    ordered_meals = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ('ordered_meals',)

class ChecksSerializer(serializers.ModelSerializer):

    #orderid = OrdersSerializer()
    meals = MealsToOrderSerializer(read_only=True)
    totalsum = serializers.FloatField(source='get_total_sum', read_only=True)
    
    class Meta:
        model = Check
        fields = ('order', 'date', 'servicefee', 'totalsum', 'meals')

    def create(self, validate_data):
        order = validated_data['order']['id']
        order.isitopen = False
        order.save()
        checks = Check.objects.create(order=order, percentage = ServicePercentage.objects.all()[0], **validated_data)
        checks.save()
        return checks
