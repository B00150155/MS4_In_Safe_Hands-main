from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    '''
    This details the registered users profile form
    '''
    class Meta:
        '''
        Lists the fields to display on the user checkout form
        '''
        model = UserProfile
        # User is excluded from the checkout form
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        '''
        Placeholders to be added to the checkout fields
        '''
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_email': 'Email Address',
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County/Locality',
            'default_eircode': 'Eircode/Postcode',
            'default_country': 'Country',
        }

        # Form will auto start on first name
        self.fields['default_email'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                # Asterisk will appear on required fields
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Set placeholders
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Labels set to false as they are not being used
            self.fields[field].label = False
