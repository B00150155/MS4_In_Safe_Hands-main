from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models


class UserProfile(models.Model):
    '''
    Unique user profile model for maintaining delivery information and order \
    history. Address, contact details and username.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_email = models.EmailField(max_length=254, null=True, blank=True)
    default_phone_number = models.CharField(max_length=20, null=True,
                                            blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True,
                                            blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_eircode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Select Country', null=True,
                                   blank=True)

    def __str__(self):
        '''
        Renames the instances of the model with the title username
        '''
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    '''
    Create a user profile if none exists or update if it does exist
    '''
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
