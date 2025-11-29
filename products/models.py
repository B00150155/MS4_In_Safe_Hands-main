from django.db import models
# from django.contrib.auth.models import User


class Category(models.Model):
    '''
    The Category model and the individual details each category will have
    '''
    class Meta:
        '''
        This will correct the verbose spelling in Django admin to the correct\
        plural spelling of categories
        '''
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=200, blank=False)
    friendly_name = models.CharField(max_length=200, null=True,
                                     blank=True)

    def __str__(self):
        '''
        Renames the instance of the Category model with the category name
        '''
        return self.name

    def get_friendly_name(self):
        '''
        To return the friendly name of the category in the Django admin
        '''
        return self.friendly_name


class Product(models.Model):
    '''
    The Product model and the individual details each product will have
    '''
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    p_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    # Always use DecimalField for money. Even simple operations like addition
    # and subtraction are not immune to float rounding issues
    # https://stackoverflow.com/questions/2569015/django-floatfield-or-decimalfield-for-currency
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        '''
        Renames the instance of the Product model with the Product name
        '''
        return self.name
