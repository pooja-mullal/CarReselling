from django.db import models


# Create your models here.
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
    approve = models.CharField(max_length=100, default='approve')
    user_type = models.CharField(max_length=300, default='user')
    contact_no = models.CharField(max_length=300, default='')

class CarDetails(models.Model):
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description =models.CharField(max_length=100)
    image = models.ImageField(upload_to='bikes/')
    available=models.CharField(max_length=100,default='True')


class Booking_details(models.Model):
    seller_id=models.CharField(max_length=100,default='0')
    user_id=models.ForeignKey('NewUser', on_delete=models.CASCADE)
    car_id=models.ForeignKey('CarDetails', on_delete=models.CASCADE)
    name=models.CharField(max_length=100,default='xyz')
    email=models.CharField(max_length=100,default='xyz')
    phone_no=models.CharField(max_length=100,default='xyz')
    address=models.CharField(max_length=100,default='xyz')
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,default='pending')

class LikedCar(models.Model):
    user_id=models.ForeignKey(NewUser, on_delete=models.CASCADE,default='1')
    bike_id = models.ForeignKey('CarDetails', on_delete=models.CASCADE)
   

    

   