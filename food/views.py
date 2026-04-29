

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    query = request.GET.get('q', '')
    if query:
        menu = Menu.objects.filter(title__icontains=query)
    else:
        menu = Menu.objects.all()

    context = {
        'menu': menu,
        'query': query,
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

@login_required(login_url='signin')
def displaycart(request):
    trolley = Cart.objects.filter(user=request.user)
    subtotal = sum(item.amount for item in trolley)
    vat = subtotal * 0.075
    total = subtotal + vat
    profile = None
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        pass
    context = {
        'trolley': trolley,
        'subtotal': subtotal,
        'vat': vat,
        'total': total,
        'profile': profile,
    }
    return render(request, 'displaycart.html', context)

@login_required(login_url='signin')
def shopcart(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Menu.objects.get(pk=menu_id)
        # Check if item already in cart — update quantity instead of duplicating
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, f'{product.title} added to cart!')
    return redirect('displaycart')

@login_required(login_url='signin')
def deleteitem(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        Cart.objects.filter(id=item_id, user=request.user).delete()
        messages.success(request, 'Item removed from cart.')
    return redirect('displaycart')

@login_required(login_url='signin')
def increase(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemid')
        new_qty = int(request.POST.get('quant', 1))
        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            cart_item.quantity = new_qty
            cart_item.save()
        except Cart.DoesNotExist:
            pass
    return redirect('displaycart')

@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        # Clear the user's cart after payment
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Payment successful! Your order is being prepared.')
    return render(request, 'callback.html')


def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 2:
        items = Menu.objects.filter(title__icontains=query)[:6]
        for item in items:
            results.append({
                'id': item.id,
                'title': item.title,
                'price': item.price,
                'img': item.img.url if item.img else '',
            })
    return JsonResponse({'results': results})
