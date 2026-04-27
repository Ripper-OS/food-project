from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Menu(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to = 'menu', default='prod.jpg')
    price = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField(default=1, editable=False)
    display = models.BooleanField()
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    dessert = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'menu'
        managed = True
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'

STATUS = [
    ('new', 'new'), 
    ('pending', 'pending'), 
    ('processing', 'processing'), 
    ('resolved', 'resolved')
]

class Contact(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=30)
    message = models.TextField()
    admin_note = models.TextField()
    status = models.CharField(max_length=50, choices = STATUS, default= 'new')
    message_date = models.DateTimeField(auto_now_add=True)
    admin_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, default = 1)
    first_name = models.CharField(max_length = 50,)
    last_name = models.CharField(max_length = 50,)
    email = models.EmailField(max_length = 50,)
    phone = models.CharField(max_length = 20,)
    address = models.CharField(max_length = 255,)
    state = models.CharField(max_length = 255,)
    pix = models.ImageField(upload_to='profile', default = 'avatar.png')  #optional: to inherit default image avater

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
