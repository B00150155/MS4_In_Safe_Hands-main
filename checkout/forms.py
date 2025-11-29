from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    '''
    This sets the fields that will be used on the order form and also sets \
    the placeholders for each field
    '''
    class Meta:
        '''
        Fields to dispaly on the checkout form
        '''
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'county', 'eircode', 'country',)

    def __init__(self, *args, **kwargs):
        # Placeholders to be added to the checkout fields
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number - no spaces between digits',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County/Locality',
            'eircode': 'Eircode/Postcode',
        }

        # Form will auto start on first name
        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                # Asterisk will appear on required fields
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Set placeholders
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Labels set to false as they are not being used
            self.fields[field].label = False
