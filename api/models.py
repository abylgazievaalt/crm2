from django.db import models

class Table(models.Model):

    name = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.name)

class Role(models.Model):

    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return str(self.name)

class Department(models.Model):
    
    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return str(self.name)

class User(models.Model):

    name = models.CharField(max_length = 20)
    surname = models.CharField(max_length = 20)
    login = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.EmailField()
    roleid = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    dateofadd = models.DateTime(default=datetime.now, blank=True)
    phone = models.CharField(max_length = 30)

    def __str__(self):
        return "%s \n %s \n %s \n %s \n %s \n %s \n %s" % (self.name, self.surname, self.login, self.email, self.roleid, self.dateofadd, self.phone)

class Category(models.Model):

    name = models.CharField(max_length=30)
    departmentid = models.ForeignKey(Department,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s %s" % (self.name, self.departmentid)

class Status(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

class ServicePercentage(models.Model):

    percentage = models.IntegerField()

    def __str__(self):
        return str(self.percentage)

class Meal(models.Model):

    name = models.CharField(max_length=50)
    categoryid = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    mealstoorder = models.ForeignKey('Meal', related_name='meals', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "%s \n %s \n %s \n %s" % (self.name, self.categoryid, self.price, self.description)

class Order(models.Model):

    waiterid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tableid = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
# tablename =

    isitopen = models.BooleanField(default=True)
    date = models.DateTime(default=datetime.now, blank=True)
#   mealsid =

class Check(models.Model):
   
   orderid = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    date = models.DateTime(default=datetime.now, blank=True)
    servicefee = models.ForeignKey(ServicePercentage, on_delete=models.CASCADE, null=True)
    totalsum = models.IntegerField()

class MealsToOrder(models.Model):

    uniqueid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
#    meals =
