import uuid
import json


from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from . models import *
from . forms import *

# Create your views here.
def index(request):
    breakfast = Menu.objects.filter(breakfast=True)
    lunch = Menu.objects.filter(lunch=True)
    dinner = Menu.objects.filter(dinner=True)
    dessert = Menu.objects.filter(dessert=True)

    context = {
        'breakfast' : breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'dessert': dessert,
    }

    return render(request, 'index.html', context)

def menu(request):
    menu = Menu.objects.all()

    context = {
        'menu':menu,
    }
    return render(request, 'menu.html', context)

def details(request, id):
    detail = Menu.objects.get(pk=id)
    context = {
        'detail':detail,
    }

    return render(request,'details.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'message delivered')
            return redirect('contact')
    return render(request, 'contact.html')

            
def about(request):
    return render(request, 'about.html')
            
def services(request):
    return render(request, 'services.html')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            newprofile = Profile(user=newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.address = address
            newprofile.state = state
            newprofile.pix = pix
            newprofile.save()
            login(request,newuser)
            messages.success(request,'Signup successfull')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request,username=username,password=passwrodd)
        if user is not None:
            login(request, user)
            messages.success(request,'Signin successful')
            return redirect('index')
        else:
            messages.error(request, 'Username/Password incorrect. Kindly supply correct details.')
            return redirect('signin')
    return render(request,'signin.html')

@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile':profile,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    profile=Profile.objects.get(user__username = request.user.username)
    update=ProfileUpdate(instance=request.user.profile)#instantiatethe form for a GET request along with the user's name
    if request.method=='POST':
        update = ProfileUpdate(request.POST, request.FILES, instance= request.user.profile)
        if update.is_valid():
            update.save()
            messages.success(request,'Profile update successful')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profile_update')
    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html',context)

def displaycart(request):
    return render(request, 'displaycart.html')

def shopcart(request):
    return redirect('displaycart')

def deleteitem(request):
    return redirect('displaycart')

def increase(request):
    return redirect('displaycart')

def pay(request):
    return render(request, 'callback.html')
