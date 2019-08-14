from django.db import models
from django.utils.timezone import datetime, timedelta
import jwt
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):
    def create_user(self, role, name, surname, username, email, phone=None, password=None):
        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email address')

        user = self.model(role=role, username=username,  email=self.normalize_email(email), name=name, surname=surname, phone=phone)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, name, surname, password=None, phone=None):
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(username=username, email=email, password=password, phone=phone, name=name, surname=surname)
        user.is_superuse = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(db_index=True, max_length = 50)
    surname = models.CharField(db_index=True, max_length = 50)
    username = models.CharField(db_index=True, max_length = 255, unique=True)
    #password = models.CharField(max_length = 50)
    email = models.EmailField(db_index=True, unique=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    dateofadd = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length = 50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return "%s %s" % (self.name, self.surname)

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id':self.pk,
            'exp':int(dt.strftime('%s'))
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

