from django.test import TestCase
from .forms import ContactMessagesForm
from contact_us import apps
from django.urls import reverse, resolve
from contact_us.views import contact_us


class TestContactMessagesForm(TestCase):
    '''
    Tests to be carried out on the registered/logged in users contact form
    '''
    def test_contact_us_page(self):
        '''
        Test to confirm correct contact us template page is rendering
        '''
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us/contact_us.html')

    def test_contact_us_url_is_resolved(self):
        '''
        Test to check contact us urls.py configured correctly
        '''
        url = reverse('contact_us')
        self.assertEquals(resolve(url).func, contact_us)

    def test_contact_us_form_sender_required(self):
        '''
        Test to confirm that 'sender' field is required on the message form. \
        This field autopopulates with the users username and the user \
        has no way to adjust this field so it shouldn't be able to leave \
        this blank
        '''
        form = ContactMessagesForm({
                                    'sender': '',
                                    'subject': 'subject',
                                    'message': 'message',
                                    'contact_email': 'contact_email',
                                   })
        self.assertFalse(form.is_valid())

    def test_contact_us_form_subject_required(self):
        '''
        Test to confirm that the 'subject' field is required on the message \
        form. A user must input a subject manually in this field. If they \
        do not then the form should be invalid.
        '''
        form = ContactMessagesForm({
                                    'sender': 'sender',
                                    'subject': '',
                                    'message': 'message',
                                    'contact_email': 'contact_email',
                                   })
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors.keys())

    def test_contact_us_form_message_required(self):
        '''
        Test to confirm that the 'message' field is required on the message \
        form. A user must input a message manually in this field.
        '''
        form = ContactMessagesForm({
                                    'sender': 'sender',
                                    'subject': 'subject',
                                    'message': '',
                                    'contact_email': 'contact_email',
                                   })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors.keys())

    def test_contact_us_form_email_not_required(self):
        '''
        Test to confirm that the 'contact email' field is not required on \
        the message form and the form will send if the field is left blank
        '''
        form = ContactMessagesForm({
                                    'subject': 'subject',
                                    'message': 'message',
                                    'contact_email': ''
                                  })
        self.assertTrue(form.is_valid())

    def test_contact_us_apps_configuration(self):
        '''
        Test to make sure the app is configured correctly
        '''
        self.assertEqual(apps.ContactUsConfig.name, 'contact_us')
