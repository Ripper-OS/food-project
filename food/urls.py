from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('details/<str:id>', views.details, name='details'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('profile', views.profile, name='profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('displaycart', views.displaycart, name='displaycart'),
    path('shopcart', views.shopcart, name='shopcart'),
    path('deleteitem', views.deleteitem, name='deleteitem'),
    path('increase', views.increase, name='increase'),
    path('pay', views.pay, name='pay'),
]
