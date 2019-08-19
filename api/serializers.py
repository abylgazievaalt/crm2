from api.models import *
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return Usre.objects.create_user(**validated_data)

class UsersSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'username',
          'password', 'email', 'created_at', 'phone']
        read_only_fields = ('token',)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if  email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

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

    id = serializers.PrimaryKeyRelatedField(
        queryset=Meal.objects.all(),
        source='meal.id'
    )
    name = serializers.CharField(
        source='meal.name',
        read_only=True
    )
    price = serializers.FloatField(
        source='meal.price',
        read_only=True
    )
    total = serializers.FloatField(
        source='get_cost',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'count', 'price', 'total')

class OrderItemSerializer2(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(
        queryset=Meal.objects.all(),
        source='meal.id'
    )
    name = serializers.CharField(
        source='meal.name',
        read_only=True
    )
                                            
    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'count')


class OrdersSerializer(serializers.ModelSerializer):
    waiterid = serializers.IntegerField(
        source='waiter.id',
        read_only=True
    )
    tableid = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        source='table.id',
    )
    tablename = serializers.CharField(
        source='table.name',
        read_only=True
    )
    meals = OrderItemSerializer2(many=True, required=False)
    
    class Meta:
        model = Order
        fields = ('id','waiterid', 'tableid',
                      'tablename', 'isitopen', 'date', 'meals')

    def create(self, validated_data):
        order = Order.objects.create(
            isitopen=True,
            table=validated_data['table']['id']
        )
            
        for meal in validated_data['meals']:
            OrderItem.objects.create(
                    order=order,
                    meal=meal['meal']['id'],
                    count=meal['count']
            ).save()
        
        order.save()
        return order

class MealsToOrderSerializer(serializers.ModelSerializer):
    
    meals = OrderItemSerializer2(many=True)
    
    class Meta:
        model = Order
        fields = ('meals',)

    def create(self, validated_data):
        order = Order.objects.get(id=validated_data['id'])
        for meal in validated_data['meals']:
            OrderItem.objects.create(
                order=order,
                meal=meal['meal']['id'],
                count=meal['count']
            ).save()

        order.save()
        return order

class MealsInCheckSerializer(serializers.ModelSerializer):
    
    meals = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ('meals',)
    
    def create(self, validated_data):
        order = Order.objects.get(id=validated_data['id'])
        for meal in validated_data['meals']:
            OrderItem.objects.create(
                 order=order,
                 meal=meal['meal']['id'],
                 count=meal['count']
            ).save()
        
        order.save()
        return order

class ChecksSerializer(serializers.ModelSerializer):

    orderid = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source='order.id'
    )

    order = MealsInCheckSerializer(read_only=True)
    totalsum = serializers.FloatField(source='get_total_sum', read_only=True)
    
    class Meta:
        model = Check
        fields = ('id', 'orderid', 'date', 'servicefee', 'totalsum', 'order')

    def create(self, validated_data):
        checks = Check.objects.create(
            order=validated_data['order']['id'],
            servicefee = ServicePercentage.objects.all()[0])
        checks.save()
        return checks
