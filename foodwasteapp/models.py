from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stored_password = models.CharField(max_length=100)  
    mobile_number = models.CharField(max_length=15)
    hotel_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)




class FoodEntry(models.Model):
    food_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    date = models.DateTimeField()
    address = models.CharField(max_length=200)
    link = models.URLField()
    userr = models.CharField(max_length=100)



class completed(models.Model):
    food_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    address = models.CharField(max_length=200)
    link = models.URLField()
    userr = models.CharField(max_length=100)
    ruser = models.CharField(max_length=100)
    source = models.CharField(max_length=100)