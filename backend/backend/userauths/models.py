from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from shortuuid.django_fields import ShortUUIDField

import logging
logger = logging.getLogger(__name__)

""""
custom user model name can be anything.
extending the AbstractUser model.
"""
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    
    USERNAME_FIELD = 'email' # login with email and password
    REQUIRED_FIELDS = ['username']
    
    # string representation of this object
    def __str__(self):
        return self.email
    
    # override the save() method
    def save(self, *args, **kwargs):
        email_username, mobile = self.email.split("@")[0], self.phone
        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User, self).save(*args, **kwargs) # for security pupose sending args,kwargs

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image", 
                            default="default/default.jpg", 
                            null=True, 
                            blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijk") # profile id

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
     # override the save() method
    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.full_name


        super(Profile, self).save(*args, **kwargs) # for security pupose sending args,kwargs


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Creating profile for user {instance.email}")
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



