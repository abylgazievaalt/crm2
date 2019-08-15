from django.db import models
from django.utils.timezone import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given login must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    role = models.ForeignKey('Role', null=True, on_delete=models.SET_NULL)
    name = models.CharField(db_index=True, max_length=255)
    surname = models.CharField(db_index=True, max_length=255)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def get_full_name(self):
        return self.name + " " + self.surname
    
    def get_short_name(self):
        return self.name
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        
        token = jwt.encode({
                           'id': self.pk,
                           'exp': int(dt.strftime('%s'))
                           }, settings.SECRET_KEY, algorithm='HS256')
                           
        return token.decode('utf-8')

class Table(models.Model):

    name = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.name)

class Role(models.Model):

    name = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.name)

class Department(models.Model):

    name = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.name)

class Category(models.Model):
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=200)
    
    class Meta:
        default_related_name="Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class ServicePercentage(models.Model):

    percentage = models.IntegerField(default=0)

    def __str__(self):
        return str(self.percentage)

class Status(models.Model):
    
    #order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name)

class Meal(models.Model):

    name = models.CharField(max_length=50)
    categoryid = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    waiterid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    isitopen = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.meals_order.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='ordered_meals', on_delete=models.CASCADE, null=True)
    meal =  models.ForeignKey(Meal,on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=1)
    
    def get_cost(self):
        return self.meal.price * self.count


class Check(models.Model):
    #waiter = models.ForeignKey(User, related_name='Checks', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='Checks')
    date = models.DateTimeField(auto_now_add=True)
    servicefee = models.ForeignKey(ServicePercentage, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Check'
        verbose_name_plural = 'Checks'
        default_related_name = 'checks'
    
    def get_total_sum(self):
        return self.order.get_total_cost() + self.servicefee.percentage

    def __str__(self):
        return "%s, %s, %s, %s" % (self.orderid, self.date, self.servicefee, self.totalsum)

