from django.test import TestCase, Client
from .models import *
from .serializers import *
import unittest
from rest_framework.test import APITestCase, APIRequestFactory
from random_word import RandomWords

r = RandomWords()

class TableTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.table = Table.objects.create(name='test Table #')
    
    def test_is_instance(self):
        self.assertIsInstance(self.table, Table)
    
    def test_table_str(self):
        self.assertEqual(str(self.table), "test Table #")

    def test_create_todo(self):
        response = self.client.post('/table/', {
                                    "name": "test name"
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/table/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/table/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_tables(self):
        response = self.client.get('/table/')
        tables = Table.objects.all()
        serializer = TablesSerializer(tables, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class RoleTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(name='test Waiter')
    
    def test_is_instance(self):
        self.assertIsInstance(self.role, Role)
    
    def test_role_name(self):
        self.assertEqual(self.role.name, "test Waiter")
    
    def test_course_str(self):
        self.assertEqual(str(self.role), "test Waiter")

    def test_create_todo(self):
        response = self.client.post('/role/', {
                                    "name": "chef"
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/role/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/role/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_roles(self):
        response = self.client.get('/role/')
        roles = Role.objects.all()
        serializer = RolesSerializer(roles, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class DepartmentTestCase(unittest.TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='test Department #')
        self.client = Client()
    
    def test_department_name(self):
        self.assertEqual(self.department.name, "test Department #")
    
    def test_is_instance(self):
        self.assertIsInstance(self.department, Department)
    
    def test_department_str(self):
        self.assertEqual(str(self.department), "test Department #")
    
    def test_create_todo(self):
        response = self.client.post('/department/', {
                                    "name": "test department"
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/department/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/department/100000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_departments(self):
        response = self.client.get('/department/')
        departments = Department.objects.all()
        serializer = DepartmentsSerializer(departments, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        department = Department.objects.create(name='test Department for category')
        self.category = Category.objects.create(name='test Desserts')
    
    def test_category_name(self):
        self.assertEqual(self.category.name, "test Desserts")
    
    def test_category_str(self):
        self.assertEqual(str(self.category), "test Desserts")

    def test_create_todo(self):
        response = self.client.post('/category/', {
                                    "name": "test category",
                                    "department": 1
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/category/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/category/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_categories(self):
        response = self.client.get('/category/')
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class ServicePercentageTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.servicefee = ServicePercentage.objects.create(percentage=20)
    
    def test_is_instance(self):
        self.assertIsInstance(self.servicefee, ServicePercentage)
    
    def test_servicepercentage_name(self):
        self.assertEqual(self.servicefee.percentage, 20)
    
    def test_servicepercentage_str(self):
        self.assertEqual(str(self.servicefee), "20")

    def test_create_todo(self):
        response = self.client.post('/servicepercentage/', {
                                    "percentage": 25
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/servicepercentage/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/servicepercentage/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_servicefees(self):
        response = self.client.get('/servicepercentage/')
        servicefees = ServicePercentage.objects.all()
        serializer = ServicePercentageSerializer(servicefees, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class MealTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.get(id=4)
        self.meal = Meal.objects.create(name="Tiramisu", price=200, description="Served with chocolate pieces.", categoryid=self.category)
    
    def test_meal_attributes(self):
        self.assertEqual(self.meal.name, 'Tiramisu')
        self.assertEqual(self.meal.price, 200)
        self.assertEqual(self.meal.description, 'Served with chocolate pieces.')
        self.assertEqual(self.meal.categoryid.id, self.category.id)

    def test_is_instance(self):
        self.assertIsInstance(self.meal, Meal)

    def test_create_todo(self):
        response = self.client.post('/meal/', {
                                    "name": "3 shokolada",
                                    "price": 230,
                                    "description": "White, milk and dark chocolate.",
                                    "categoryid": 3
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/meal/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/meal/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_meals(self):
        response = self.client.get('/meal/')
        meals = Meal.objects.all()
        serializer = MealsSerializer(meals, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    #def test_create_todo(self):
    #  response = self.client.post('/order/', {
    #                              "tableid": 1,
    #                                "meals" : [
    #                                          {
    #                                          "id": 1,
    #                                          "count": 3
    #                                          },
    #                                          {
    #                                          "id": 2,
    #                                          "count": 1
    #                                          }
    #                                          ]
    #                                })
    #   self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/order/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/order/10000/')
        self.assertEqual(response.status_code, 404)

    def test_list_orders(self):
        response = self.client.get('/order/')
        orders = Order.objects.all()
        serializer = OrdersSerializer(orders, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_create_todo(self):
        id = Order.objects.last().id
        response = self.client.post('/check/', {
                                    "orderid": id,
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/check/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/check/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_checks(self):
        response = self.client.get('/check/')
        checks = Check.objects.all()
        serializer = ChecksSerializer(checks, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_create_todo(self):
        id = Order.objects.last().id
        response = self.client.post('/check/', {
                                    "orderid": id,
                                    })
        self.assertEqual(response.status_code, 201)
    
    def test_details(self):
        response = self.client.get('/check/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/check/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_list_checks(self):
        response = self.client.get('/check/')
        checks = Check.objects.all()
        serializer = ChecksSerializer(checks, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_details(self):
        response = self.client.get('/user/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_not_found(self):
        response = self.client.get('/user/10000/')
        self.assertEqual(response.status_code, 404)
    
    #def test_list_users(self):
    #   response = self.client.get('/user/')
    #   users = User.objects.all()
    #   serializer = UsersSerializer(users, many=True)
        
        #self.assertEqual(response.data, serializer.data)
        #self.assertEqual(response.status_code, 200)

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_post_response(self):
        rand = r.get_random_word()
        response = self.client.post('/signup/', {
                                    "email": rand + "@gmail.com",
                                    "username": rand,
                                    "password": "password12"
                                    })
        self.assertEqual(response.status_code, 201)

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_post_response(self):
        response = self.client.post('/login/', {
                                    "email": "ab@gmail.com",
                                    "password": "password123"
                                    })
        self.assertEqual(response.status_code, 200)
