# from random import choices
# from telnetlib import STATUS
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Contact(models.Model):
    Status = [
    ('new', 'new'),
    ('pending', 'pending'),
    ('processing', 'processing'),
    ('resolved', 'resolved')
    ]
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20, default='a')
    message = models.TextField()
    admin_note = models.TextField()
    status = models.CharField(max_length=50, choices=Status,  default='new')
    message_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)


    def ___str___(self):
        return self.full_name


    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'    


class Product(models.Model):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to= 'product', default='prod.jpg')
    price = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    display = models.BooleanField()
    trending = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)    

    def ___str___(self):
        return self.name


    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'            


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pix = models.ImageField(upload_to= 'profile', default= 'avatar.png')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'   

class Shopcart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    order_no = models.CharField(max_length=255)
    paid = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)   


    def __str__(self):
        return self.products.name    