from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from sre_parse import CATEGORIES
from tkinter import CASCADE
from turtle import update
from unicodedata import category, decimal

from django.db import models


from django.conf import settings
# from django.contrib.auth.models import User



# Create your models here.

class Room(models.Model):
    CATEGORIES = {
        ('eco','economy'),
        ('fam','family'),
        ('roy','royal'),
        ('bus','business'),
    }
 
    number = models.IntegerField(blank=True,null=True)
    category = models.CharField(max_length=3, choices=CATEGORIES)
    beds = models.IntegerField(default=1,blank=True)
    image = models.ImageField()
    update = models.DateTimeField(auto_now_add=True)
    capacity = models.BooleanField(max_length=100)


    def __str__(self):
        return f'{self.number}. {self.category} with {self.beds} beds for {self.capacity} people'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'



class Contact(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    message_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)
    admin_note = models.TextField()
    phone = models.CharField(max_length=20)
      


    def __str_(self):
        return self.username


class Profile(models.Model):
    username = models.CharField(max_length=50)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='profile', default='avatar.png')
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username



class Shopcart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name_id  = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    amount = models.IntegerField(blank=True, null=True)
    order_no = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room.name