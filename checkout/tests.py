from django.test import TestCase
from django.urls import reverse, resolve
from checkout import apps
from checkout.views import checkout, cache_checkout_data
from checkout.webhooks import webhook


class TestCheckout(TestCase):
    '''
    Tests for the checkout page
    '''
    def test_checkout_page(self):
        '''
        If the user has nothing in the shopping cart and attempts to access \
        the checkout page they will be redirected to the products page
        '''
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')

    def test_checkout_apps_configuration(self):
        '''
        Test to make sure the app is configured correctly
        '''
        self.assertEqual(apps.CheckoutConfig.name, 'checkout')

    def test_checkout_url_is_resolved(self):
        '''
        Test to check checkout urls.py configured correctly
        '''
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_webhook_url_is_resolved(self):
        '''
        Test to check webhook urls.py configured correctly
        '''
        url = reverse('webhook')
        self.assertEquals(resolve(url).func, webhook)

    def test_cache_checkout_data_url_is_resolved(self):
        '''
        Test to check cache_checkout_data urls.py configured correctly
        '''
        url = reverse('cache_checkout_data')
        self.assertEquals(resolve(url).func, cache_checkout_data)
