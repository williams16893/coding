from importlib.resources import contents
from multiprocessing import context
from operator import itemgetter
import re
from tkinter.tix import Form
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View



from . forms import *
from . models import *



# Create your views here.
def index(request):
    latest = Product.objects.filter(latest=True).order_by('-price')
    trending = Product.objects.filter(trending=True).order_by('price')

    context = {
        'vic':latest,
        'math':trending,
    }

    return render(request, 'index.html', context)


def contact(request):
    form = ContactForm()#instatiate the contactform for a GET request
    if request.method == 'POST': #make a POST REQUEST
        form = ContactForm(request.POST)    #instatiate the contactform for a POST request
        if form.is_valid():#Django will validate the form
            form.save()#if validate, save the data to the DB
            messages.success(request, 'I have received your message.')
            return redirect('index')#return to index once the post action is carried out
    return render(request, 'contact.html')
    # return HttpResponse('Contact done')

















def products(request):
    product = Product.objects.all()

    context = {
        'product':product,
    }
    return render(request, 'products.html',context)


def details(request, id):
    detail = Product.objects.get(pk=id)
    context = {
        'detail':detail,
    }
    return render(request, 'details.html',context)




# authentication
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        usernamee = request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request,username= usernamee, password=passwrodd)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signin successfull')
            return redirect('index')
        else:
            messages.warning(request, 'Username/Password incorrect. kindly supply valid details')
            return redirect('signin')
    return render(request, 'signin.html')


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
            newprofile = Profile(user = newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.address = address
            newprofile.state = state
            newprofile.pix = pix
            newprofile.save()
            login(request, newuser)
            messages.success(request, 'Signup successful')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')
# authentication done


# profile
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username=request.user.username)
    context = {
        'profile':profile,
    }
    return render(request, 'profile.html',context)


@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username =request.user.username)
    update = ProfileUpdate(instance = request.user.profile)
    if request.method == 'POST':
        update = ProfileUpdate(request.POST, request.FILES, instance = request.user.profile)
        if update.is_valid():
            update.save()
            messages.success(request, 'Profile update successful!')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profile_update')
    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password(request):
    profile = Profile.objects.get(user__username=request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password change successful.')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')
    context = {
        'form':form
    }
    return render(request, 'password.html', context)
# profile done

# shopcart
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        item_id = request.POST['product_id']
        item = Product.objects.get(pk=item_id)
        order_num = Profile.objects.get(user__username = request.user.username)
        cart_no = order_num.id

        cart = Shopcart.objects.filter(user__username = request.user.username, paid= False)#Shopper with items
        if cart:# existing order(object) with a selected item quantity to be incremented
            basket = Shopcart.objects.filter(product = item.id, user__username= request.user.username).first()
            if basket:
                basket.quantity += quant
                basket.amount = basket.price  * quant
                basket.save()
                messages.success(request, 'Item added to cart.')
                return redirect('products')
            else:
                newitem = Shopcart()
                newitem.user = request.user
                newitem.product = item
                newitem.name_id = item.title
                newitem.quantity =quant
                newitem.price = item.price
                newitem.amount = item.price * quant
                newitem.order_no = cart_no
                newitem.paid = False
                newitem.save()
                messages.success(request, 'Item added to cart.')
                return redirect('products')
        else:
            newcart = Shopcart()#create a new shopcart
            newcart.user = request.user
            newcart.product = item
            newcart.name_id = item.title
            newcart.quantity = quant
            newcart.price = item.price
            newcart.price = item.price * quant
            newcart.order_no = cart_no
            newcart.paid = False  
            newcart.save()
            messages.success(request, 'Item added to Shopcart.')
            return redirect('products')
    return redirect('products')


def displaycart(request):
    trolley = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal = cart.price * cart.quantity

    vat = 0.075 * subtotal

    total = vat + subtotal


    context = {
        'trolley':trolley,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    return render(request, 'displaycart.html',context)


def deleteitem(request):
    item_id = request.POST['item_id']
    item_delete = Shopcart.objects.get(pk=item_id)
    item_delete.delete()
    messages.success(request, 'Item deleted successfully.')
    return redirect('displaycart')

def increase(request):
    if request.method == 'POST':
        the_item = request.POST['itemid']
        the_quant = int(request.POST['quant'])
        modify = Shopcart.objects.get(pk=the_item)
        modify.quantity += the_quant
        modify.save()
    return redirect('displaycart')


# checkout using class based view and axios get request
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid=False)
        context = {
            'summary':summary
        }
        return render(request, 'checkout.html', context)
# checkout using class based view and axios get request done
    
#shopcart done
def callback(request):
    profile = profile.objects.get(user__username = request.user.username)
    cart = shopcart.objects.filter(user__username = request.user.username, paid=False)


    
