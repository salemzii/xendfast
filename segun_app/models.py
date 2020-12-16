from django.db import models
from django.contrib.auth.models import User 


class rate(models.Model):
    name = models.CharField(max_length=20, default='Naira Price')
    exchange_rate = models.IntegerField(default=365)

    def __str__(self):
        return self.name


class kycinfo(models.Model):
    Link = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='No name')
    home_address = models.CharField(max_length=200, default='None')
    phone_number = models.IntegerField(default=0000)
    personal_ids = models.ImageField(default='default.jpg', upload_to='profile_pics')
    dob = models.DateField(default='12/12/2000')
    is_verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name


# Create your models here.
