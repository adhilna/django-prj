from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .filter import OrderFilter
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='loginpage')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_ordered = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outfordelivery = orders.filter(status='Out for Delivery').count()
    context = {'customers':customers, 'orders':orders, 'total_ordered':total_ordered, 'delivered':delivered, 'pending':pending, 'outfordelivery':outfordelivery}
    return render(request, 'dashboard.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin'])
def customer(request, pk):
    # can write inthis way
    customer = Customer.objects.get(id=pk)  
    orders = customer.order_set.all()

    orderFilter = OrderFilter(request.GET)
    orders = orderFilter.qs

    order_count = orders.count()
    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'orderFilter':orderFilter}
    return render(request, 'customer.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin'])
def createOrder(request):
    form = OrderForm
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'order_form.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin'])
def updateOrder(request, pk):
    # or in this way : this is the std way
    order = get_object_or_404(Order, id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'order_form.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin'])
def deleteOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request, 'delete.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or Password is incorrect")
    context = {}
    return render(request, 'login.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                )
            messages.success(request, "Account was created for " + username)
            return redirect('loginpage')
    context = {'form':form}
    return render(request, 'register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_ordered = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    outfordelivery = orders.filter(status='Out for Delivery').count()
    context = {'orders':orders, 'total_ordered':total_ordered, 'delivered':delivered, 'pending':pending, 'outfordelivery':outfordelivery}
    return render(request, 'user.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customer'])
def customerProfile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            print(request.user.profilepic)  # or request.user.profile.profilepic if in a related model

    context = {'form':form}
    return render(request, 'customer_profile.html', context)