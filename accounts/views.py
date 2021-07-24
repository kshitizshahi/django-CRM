from django.shortcuts import render, redirect
from accounts.models import Customer, Product, Order, Tag
from django.forms import inlineformset_factory
from accounts.forms import OrderForm, CustomerForm, CreateUserForm
from accounts.filters import OrderFilter
from accounts.decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'customers': customers, 'orders': orders, 'total_customers': total_customers,
        'total_orders': total_orders, 'delivered': delivered, 'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'accounts/user_profile.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username Or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    # tag_list = []
    # for product in products:
    #     tag_list.extend(list(Tag.objects.filter(product__name=product)))

    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.POST, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer': customer, 'orders': orders, 'total_orders': total_orders, 'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'forms': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        formset = CustomerForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'forms': form}
    return render(request, 'accounts/create_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'forms': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order_delete': order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewTag(request, pk):
    product = Product.objects.get(id=pk)
    tags = Tag.objects.filter(product__name=product)

    final_tag = ""

    for tag in tags:

        final_tag = f"{final_tag} {tag},"
        product_tag = final_tag.rstrip(final_tag[-1])

    context = {'products': product, 'tags': product_tag}

    return render(request, 'accounts/tags.html', context)
