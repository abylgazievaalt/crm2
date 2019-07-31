from django.db import models
from django.utils.timezone import datetime
import uuid

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

class User(models.Model):

    name = models.CharField(max_length = 50)
    surname = models.CharField(max_length = 50)
    login = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    email = models.EmailField(db_index=True, unique=True)
    roleid = models.ForeignKey(Role, on_delete=models.SET_NULL)
    dateofadd = models.DateTimeField(default=datetime.now, blank=True)
    phone = models.CharField(max_length = 50)

    def __str__(self):
        return "%s %s" % (self.name, self.surname)

class MealCategory(models.Model):

    name = models.CharField(max_length=50)
    departmentid = models.ForeignKey(Department,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)

class ServicePercentage(models.Model):

    percentage = models.IntegerField(default=0)

    def __str__(self):
        return str(self.percentage)

class Meal(models.Model):
    
    name = models.CharField(max_length=50)
    categoryid = models.ForeignKey(MealCategory, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.name)

class Order(models.Model):
    waiterid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tableid = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    #tablename = Table.objects.get(id=tableid)
    isitopen = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    
    def get_total_cost(self):
        return sum(orderitem.get_total() for orderitem in self.mealsid.all())
    
    def __str__(self):
        return "%s, %s, %s, %s" % (self.tableid, self.tablename, self.isitopen, self.date)

class Status(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name)

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name='mealsid', on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(default=0)

    def get_total(self):
        return self.meal.price * self.amount

class Check(models.Model):

    orderid = models.OneToOneField(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    servicefee = models.ForeignKey(ServicePercentage, on_delete=None)
    
    def get_total_sum(self):
        return self.order.get_total_cost() + self.servicefee.percentage

    def __str__(self):
        return "%s, %s, %s, %s" % (self.orderid, self.date, self.servicefee, self.totalsum)
