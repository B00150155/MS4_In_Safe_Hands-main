from django.test import TestCase
from profiles import apps
from .forms import UserProfileForm
from django.urls import reverse, resolve
from profiles.views import profile, order_history


# Create your tests here.
class TestProfile(TestCase):
    '''
    Tests to run on the user profile page
    '''
    def test_profile_page(self):
        '''
        If the user is not logged in and attempts to access the profile page \
        they will be redirected to the login page
        '''
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_profiles_url_is_resolved(self):
        '''
        Test to check profiles urls.py configured correctly
        '''
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_order_history_url_is_resolved(self):
        '''
        Test to check order history urls.py configured correctly
        '''
        url = reverse('order_history', args=[1])
        self.assertEquals(resolve(url).func, order_history)

    def test_profiles_apps_configuration(self):
        '''
        Test to make sure the app is configured correctly
        '''
        self.assertEqual(apps.ProfilesConfig.name, 'profiles')

    def test_user_profile_form_is_valid(self):
        '''
        A test to confirm the fields that are required for the form to \
        be valid. Only the user form is a required field.
        '''
        form = UserProfileForm({
                               'user': 'user',
                               'default_email': '',
                               'default_phone_number': '',
                               'default_street_address1': '',
                               'default_street_address2': '',
                               'default_town_or_city': '',
                               'default_county': '',
                               'default_eircode': '',
                               'default_country': '',
                               })
        self.assertTrue(form.is_valid())

