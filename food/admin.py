from django.contrib import admin
from . models import *
# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img', 'price', 'max_quantity', 'min_quantity', 'display', 'created', 'update', 'description', 'breakfast', 'lunch', 'dinner', 'dessert')
admin.site.register(Menu,MenuAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','email','message','admin_note','status','message_date','admin_update')
admin.site.register(Contact,ContactAdmin)

