from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from products import apps
from products.views import (
    all_products, delete_product, product_details, add_product, edit_product)
from .models import Product, Category


# from django.test.client import Client


# Create your tests here.
class TestProducts(TestCase):
    '''
    Tests to be run on the product and product details pages
    '''
    def test_products_page(self):
        '''
        Test to confirm correct products template page is rendering
        '''
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_products_url_is_resolved(self):
        '''
        Test to check products urls.py configured correctly
        '''
        url = reverse('products')
        self.assertEquals(resolve(url).func, all_products)

    def test_product_details_url_is_resolved(self):
        '''
        Test to check product details urls.py configured correctly
        '''
        url = reverse('product_details', args=[1])
        self.assertEquals(resolve(url).func, product_details)

    def test_add_product_url_is_resolved(self):
        '''
        Test to check add product urls.py configured correctly
        '''
        url = reverse('add_product')
        self.assertEquals(resolve(url).func, add_product)

    def test_edit_product_url_is_resolved(self):
        '''
        Test to check edit product urls.py configured correctly
        '''
        url = reverse('edit_product', args=[1])
        self.assertEquals(resolve(url).func, edit_product)

    def test_delete_product_url_is_resolved(self):
        '''
        Test to check delete product history urls.py configured correctly
        '''
        url = reverse('delete_product', args=[1])
        self.assertEquals(resolve(url).func, delete_product)

    def test_product_details_page(self):
        '''
        Test to confirm correct product details template page is rendering
        '''
        product = Product.objects.create(price='1', name='Test Product')
        response = self.client.get(f'/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_details.html')

    def test_adding_product(self):
        '''
        Test to confirm if a none superuser attempts to access the add \
        product page they will be redirected to the login page
        '''
        response = self.client.post('/products/add/')
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')

    def test_products_apps_configuration(self):
        '''
        Test to make sure the app is configured correctly
        '''
        self.assertEqual(apps.ProductsConfig.name, 'products')

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test@mail.com',
            password='test_password'
        )
        self.category = Category.objects.create(
            name='test_category',
            friendly_name='test_friendly_name'
        )
        self.product = Product.objects.create(
            p_id=1,
            name='test_product',
            description='test_description',
            price='1',
            rating='1',
            image_url='www.test.com',
            image='test_image.png',
            category=self.category,
        )

    def test_category_model(self):
        '''
        Tests the Category model
        '''
        self.assertEqual(str(self.category), "test_category")

    def test_product_model(self):
        '''
        Tests the Product model
        '''
        self.assertEqual(str(self.product), "test_product")
