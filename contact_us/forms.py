from django import forms
from django.forms import ModelForm
from django.forms import HiddenInput
from .models import ContactMessages


class ContactMessagesForm(forms.ModelForm):
    '''
    This sets out how the contact form on the contact us page wil be rendered
    '''
    class Meta:
        '''
        Sets the fields that will be displayed on the contact us form
        '''
        model = ContactMessages
        fields = ('sender', 'subject', 'message', 'contact_email')
        widgets = {'sender': HiddenInput()}

    def __init__(self, *args, **kwargs):
        '''
        Placeholders to be added to the contact form
        '''
        super().__init__(*args, **kwargs)
        placeholders = {
            'sender': 'Sent by',
            'subject': 'Message subject',
            'message': 'Your message',
            'contact_email': 'Your email address',
            }

        # Form will auto start on subject
        self.fields['subject'].widget.attrs['autofocus'] = True
        for field in self.fields:
            # Asterisk will appear on required fields
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # Set placeholders
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Labels set to false as they are not being used
            self.fields[field].label = False
