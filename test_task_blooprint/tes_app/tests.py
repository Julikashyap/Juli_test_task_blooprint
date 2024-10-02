from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product, Stock
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import User

class CategoryAPITestCase(APITestCase):
    def setUp(self):
        # self.user = User.objects.create_user(username='superuser@gmail.com', password='Admin@1234')
        self.token = self.get_jwt_token()
        self.category = Category.objects.create(name='Electronics', description='Electronic items')

    def get_jwt_token(self):
        # Log in to obtain the JWT token
        login_data = {
            'username': 'superuser@gmail.com',
            'password': "Admin@1234",
        }
        response = self.client.post('v1/api/login', login_data)
        print(response.content)
        return response.data['access_token']

    def get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def test_get_categories(self):
        response = self.client.get('/api/v1/categories/', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        response = self.client.get(f'/api/v1/categories/{self.category.id}/', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {'name': 'Clothing', 'description': 'Wearable items'}
        response = self.client.post('/api/v1/categories/', data, **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        data = {'name': 'Updated Electronics', 'description': 'Updated description'}
        response = self.client.put(f'/api/v1/categories/{self.category.id}/', data, **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        response = self.client.delete(f'/api/v1/categories/{self.category.id}/', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ProductAPITestCase(APITestCase):

    def setUp(self):
        category = Category.objects.create(name='Electronics', description='Electronic items')
        self.product = Product.objects.create(name='Smartphone', category=category, price=999.99, description='Latest smartphone')

    def get_jwt_token(self):
        # Log in to obtain the JWT token
        login_data = {
            'username': 'superuser@gmail.com',
            'password': "Admin@1234",
        }
        response = self.client.post('v1/api/login', login_data)
        print(response)
        return response.data['access_token']

    def get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def test_get_products(self):
        response = self.client.get('/api/v1/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, **self.get_auth_headers())

    def test_get_product(self):
        response = self.client.get(f'/api/v1/item/{self.product.id}/', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        category = Category.objects.first()
        data = {
            'name': 'Laptop',
            'category': category.id,
            'price': 1200.00,
            'description': 'High-end laptop'
        }
        response = self.client.post('/api/v1/item/', data, **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product(self):
        data = {'name': 'Updated Smartphone', 'category': self.product.category.id, 'price': 999.99, 'description': 'Updated smartphone description'}
        response = self.client.put(f'/api/v1/item/{self.product.id}/', data, **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        response = self.client.delete(f'/api/v1/item/{self.product.id}/', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class StockAPITestCase(APITestCase):

    def setUp(self):
        # self.user = User.objects.create_user(username='superuser@gmail.com', password='Admin@1234')
        self.token = self.get_jwt_token()
        category = Category.objects.create(name='Electronics', description='Electronic items')
        product = Product.objects.create(name='Smartphone', category=category, price=999.99, description='Latest smartphone')
        self.stock = Stock.objects.create(product=product, quantity=10)
    
    def get_jwt_token(self):
        # Log in to obtain the JWT token
        login_data = {
            'username': 'superuser@gmail.com',
            'password': "Admin@1234",
        }
        response = self.client.post('v1/api/login', login_data)
        print(response)
        return response.data['access_token']

    def get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

    def test_get_stock(self):
        response = self.client.get('/api/v1/stock/', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)