from django.shortcuts import render, redirect
from django.views import View
import razorpay
from . models import Product, Customer, Cart, Payment, OrderPlaced
from . forms import UserRegisterationForm, LoginForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

# Create your views here.

def Home(request):
    return render(request, "myapp/home.html")


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = product.values('title')
        return render(request, "myapp/category.html", {'product': product, 'title': title})
    
    
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "myapp/category.html", {'product': product, 'title': title})
    
    
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "myapp/productdetail.html", {'product': product})
    
    
def Signup(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registeration Successfull")
        else:
            messages.warning(request, "Invalid Data")
    form = UserRegisterationForm()
    return render(request, 'myapp/signup.html', {'form': form})   


def Signin(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfull")
                return redirect('/profile/')
            else:
                messages.warning(request, "Invalid username or password.")
        else: 
            messages.error(request, "Please correct the errors below.")
    form = LoginForm()
    return render(request, 'myapp/signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/login')


def ProfileView(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
            return redirect('/profile/')
        else:
            messages.warning(request, "Invalid Input Data")
    form = CustomerProfileForm()
    return render(request, "myapp/profile.html", {'form': form})


def Address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "myapp/address.html", {'add': add})

def UpdateAddress(request, pk):
    add = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
            return redirect('/address/')
        else:
            messages.warning(request, "Invalid Input Data")
    form = CustomerProfileForm(instance=add)
    return render(request, "myapp/updateaddress.html", {'form': form})


def About(request):
    return render(request, "myapp/about.html")


def Contact(request):
    return render(request, "myapp/contact.html")


def AddToCart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")
    

def ShowCart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for i in cart:
        value = i.quantity * i.product.discounted_price
        amount += value
    totalamount = amount + 40
    return render(request, 'myapp/addtocart.html', {'cart': cart, 'amount': amount, 'totalamount': totalamount})


def PlusCart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
    
def MinusCart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for i in cart:
            value = i.quantity * i.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    

def RemoveCart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        if not prod_id:
            return JsonResponse({'error': 'Product ID is missing'})
        
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'})
        
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=user)).first()
        if not cart_item:
            return JsonResponse({'error': 'Product not found in cart'})
        
        cart_item.delete()
        
        cart = Cart.objects.filter(user=user)
        amount = sum(i.quantity * i.product.discounted_price for i in cart)
        totalamount = amount + 40
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
    
class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for i in cart_items:
            value = i.quantity * i.product.discounted_price
            famount += value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {'amount': razoramount, 'currency': 'INR', 'receipt': 'order_rcptid_12'}
        payment_response = client.order.create(data = data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, "myapp/checkout.html", locals())
    
    
def PaymentDone(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id = cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for i in cart:
        OrderPlaced(user=user, customer=customer, product=i.product, quantity=i.quantity, payment=payment).save()
        i.delete()
    return redirect("orders")