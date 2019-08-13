from django.db import models
from django.utils.timezone import datetime

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
    roleid = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    dateofadd = models.DateTimeField(default=datetime.now, blank=True)
    phone = models.CharField(max_length = 50)

    def __str__(self):
        return "%s %s" % (self.name, self.surname)

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
        return sum(orderitem.get_total() for orderitem in self.mealsid.all())

    def __str__(self):
        return "%s, %s, %s, %s" % (self.table, self.tablename, self.isitopen, self.date)

class Status(models.Model):

    #order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
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

