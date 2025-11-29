import uuid
from django_countries.fields import CountryField
from django.db.models import Sum
from django.conf import settings
from django.db import models
from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    '''
    This is the order model and the fields that are used in each order when \
    a user purchases something on the site
    '''
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    # full_name added to make webhook function
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    eircode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Select Country *', null=False,
                           blank=False)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def __str__(self):
        '''
        This returns the order number as the main column in the admin
        '''
        return self.order_number

    def _generate_order_number(self):
        '''
        Generate a unique, random order number using UUID
        '''
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        '''
        Override the original save method and set an order number if one \
        hasn't been set already. Also creating a user fullname by \
        concatinating first and last name.
        '''
        if not self.order_number:
            self.order_number = self._generate_order_number()
        # added 1 line below to test webhook form
        self.full_name = self.first_name + " " + self.last_name
        super().save(*args, **kwargs)

    def update_total(self):
        '''
        Update grand total each time a line item is added, accounting for \
        delivery costs.
        '''
        # The lines below (68) is longer than the 79 limit for python but
        # have been told by tutors this is ok to leave
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()


class OrderLineItem(models.Model):
    '''
    This is the order line model. This refers to the specific line order \
    item in an order. There can be several line order items and they will \
    all be rolled into 1 order
    '''
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        # Override the original save method and set line item total and
        # update the order total
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'p_id {self.product.p_id} on order {self.order.order_number}'
