from django.shortcuts import render, redirect, HttpResponse
from test001.models import *
from django.http import JsonResponse

from collections import OrderedDict  # To order dictionary
from test001.forms import *  # for login form
from django.contrib.auth import authenticate, login, logout  # for user authentication
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # To check login state
from django.http import JsonResponse  # Json response
from django.db.models import Q  # For or logic operation for filter
import datetime  # To set date
from django.contrib.auth.decorators import user_passes_test  # Django test for superuser


# Create your views here.

# ********************************* CRUD *************************************


# Show full table
def products_list(request):
    # Get full table
    info = Products.objects.values()
    return render(request, 'test.html', {'info': info})


def detailImage_list(request):
    info = DetailImage.objects.values()
    return render(request, 'test.html', {'info': info})


def customer_list(request):
    info = Customer.objects.values()
    return render(request, 'test.html', {'info': info})


def shopping_cart_list(request):
    info = Shopping_cart.objects.values()
    return render(request, 'test.html', {'info': info})


def order_list(request):
    info = Order.objects.values()
    return render(request, 'test.html', {'info': info})


def order_item_list(request):
    info = Order_Items.objects.values()
    return render(request, 'test.html', {'info': info})


# Create field
def create_products(request):
    product_id = request.POST["product_id"]
    product_type = request.POST["product_type"]
    product_name = request.POST["product_name"]
    product_price = request.POST["product_price"]
    displayimage = request.POST["displayimage"]
    brand = request.POST["brand"]
    isbn = request.POST["isbn"]
    authors = request.POST["authors"]
    publisher = request.POST["publisher"]
    release_date = request.POST["release_date"]
    num_of_pages = request.POST["num_of_pages"]
    description = request.POST["description"]
    Products.objects.create(Product_id=product_id, Product_type=product_type, Product_name=product_name,
                            Product_price=product_price, DisplayImage=displayimage, Brand=brand, ISBN=isbn,
                            Authors=authors, Publisher=publisher, Release_date=release_date, Num_of_pages=num_of_pages,
                            Description=description)


def create_detailimage(request):
    product_id = request.POST["product_id"]
    img_id = request.POST["img_id"]
    img_url = request.POST["img_url"]
    DetailImage.objects.create(Product_ID=product_id, Img_ID=img_id, Img_URL=img_url)


def create_customer(request):
    cust_id = request.POST["cust_id"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    address = request.POST["address"]
    password = request.POST["password"]
    Customer.objects.create(Cust_iD=cust_id, Email=email, First_name=first_name, Last_name=last_name, Address=address,
                            Password=password)


def create_shopping_cart(request):
    cust_id = request.POST["cust_id"]
    product_id = request.POST["product_id"]
    quantity = request.POST["quantity"]
    Shopping_cart.objects.create(Cust_ID=cust_id, Product_ID=product_id, Quantity=quantity)


def create_order(request):
    ponumber = request.POST["ponumber"]
    cust_id = request.POST["cust_id"]
    order_date = request.POST["order_date"]
    cancel_date = request.POST["cancel_date"]
    ship_date = request.POST["ship_date"]
    status = request.POST["status"]
    total_payment = request.POST["total_payment"]
    Order.objects.create(POnumber=ponumber, Cust_ID=cust_id, Order_date=order_date, Cancel_date=cancel_date,
                         Ship_date=ship_date, Status=status, total_payment=total_payment)


def create_order_item(request):
    ponumber = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=30, decimal_places=2)  # Define as decimal in dictionary / Double
    quantity = models.IntegerField(validators=[MaxValueValidator(5)])
    Order_Items.objects.create(POnumber=ponumber, Product_id=product_id, Product_price=product_price, Quantity=quantity)


# Update field by pk


# Read table by pk


# Delete a Field by pk

# ********************************* Homepage *************************************

def home_page(request):
    # B: login check login state
    if request.user.is_authenticated:
        username = request.user.get_username()
    else:
        username = ''
    context = {
        'login': request.user.is_authenticated,
        'username': username,
        'superuser': request.user.is_superuser  # E1 to disable customer buttons
    }
    return render(request, 'home_info.html', context)


# ********************************* A *************************************


# Get distinct brand
def distinct_brand():
    brand_field = Products.objects.values('Brand')
    sort = []
    for k in brand_field:
        sort.append(k['Brand'])
    sort = list(OrderedDict.fromkeys(sort))
    return sort


# To split the list of data into sections
def divide_section(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


# sort by brand by html code form
def product_list_page(request,):
    sort_by_price = request.GET.get('sort_by_price', "")
    filter_by = request.GET.get('filter_by', "")
    search = request.GET.get('product_name', "")
    search_id = request.GET.get('product_id', "")
    page_num = request.GET.get('page', "1")
    reset_btn = False
    show_table = 2 # the number of item in a section

    sort_table = Products.objects.all()
    sort = distinct_brand()

    # sort by price
    if sort_by_price != "":
        sort_table = Products.objects.order_by('Product_price')
    # filter by brand
    if filter_by != "":
        sort_table = sort_table.filter(Brand=filter_by)
    # search product name
    if search != "":
        sort_table = sort_table.filter(Product_name__icontains=search)
    # E2 search by id
    if request.user.is_superuser:
        if search_id != '':
            sort_table = sort_table.filter(Product_ID=search_id)
    if sort_by_price != "" or filter_by != "" or search != "" or search_id != '':
        reset_btn = True
    # B: login check login state
    if request.user.is_authenticated:
        username = request.user.get_username()
    else:
        username = ''

    page=[]
    section=[]
    if len(sort_table) != 0:
        true_table = sort_table
        section = list(divide_section(sort_table, show_table))
        sort_table = section[int(page_num)-1]
        page = range(1, len(section)+1)
    context = {
        'login': request.user.is_authenticated,
        'username': username,
        'info': sort_table,
        'sort': sort,
        'sort_brand_input': sort_by_price,
        'filter_input': filter_by,
        'search_input': search,
        'superuser': request.user.is_superuser,  # E1 to disable customer buttons
        'search_id': search_id, # E2 for filter id
        'reset_btn': reset_btn,
        'page': page,
        'page_num': int(page_num),
        'pre_page': int(page_num)-1,    # Django template do not support subtraction, for page previous button
        'end_page': len(section)   # for next page button
    }
    return render(request, 'A.html', context)


# Page for each product
def product_page(request, target):
    target_product = target
    DetailImage_table = DetailImage.objects.filter(Product_ID=target_product).values('Img_URL')
    Products_table = Products.objects.filter(Product_ID=target_product).values()

    # B: login check login state
    if request.user.is_authenticated:
        username = request.user.get_username()
    else:
        username = ''

    context = {
        'login': request.user.is_authenticated,
        'username': username,
        'info': Products_table,
        'img': DetailImage_table,
        'product_id': target_product,  # for add shopping cart button
        'superuser': request.user.is_superuser  # E1 to disable customer buttons
    }
    return render(request, 'A_Products.html', context)


# ********************************* B *************************************


# Load login page
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#how-to-log-a-user-in
def login_page(request):
    form = customer_login()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Success!')
            return redirect('/')
        else:
            context = {
                'form': form,
                'error': 'Invalid Username or Password'}
            return render(request, 'Login_page.html', context)
    return render(request, 'Login_page.html', {'form': form})


# Load register page
# https://stackoverflow.com/questions/3222549/how-to-automatically-login-a-user-after-registration-in-django
def register_page(request):
    user_form = CustomUserCreationForm()
    if request.method == 'POST':
        post_user_form = CustomUserCreationForm(request.POST)
        if post_user_form.is_valid():
            create = post_user_form.save()
            new_user = authenticate(
                request,
                username=post_user_form.cleaned_data['username'],
                password=post_user_form.cleaned_data['password1']
            )
            if new_user is not None:
                login(request, new_user)
                messages.success(request, 'Account created successfully')
                return redirect('/')
            else:
                return messages.success(request, 'save error, new user not created');
        else:
            # https://docs.djangoproject.com/en/3.0/ref/contrib/messages/
            return render(request, 'Register_page.html', {'user_form': post_user_form})
    return render(request, 'Register_page.html', {'user_form': user_form})


# B2: logout
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#the-login-required-decorator
@login_required  # function required user login
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Success!')
    return redirect('/')


# B3: Change password
@login_required  # function required user login
def change_password(request):
    pw_form = customer_change_pw()
    if request.method == 'POST':
        post_pw_form = customer_change_pw(request.POST)
        if post_pw_form.is_valid():
            u = User.objects.get(username=request.user.get_username())
            if u.check_password(post_pw_form.cleaned_data.get('old_password')):
                u.set_password(post_pw_form.cleaned_data.get('new_password1'))
                u.save()
                messages.success(request, 'Password successfully changed')
                return redirect('/')
            else:
                messages.success(request, 'Current Password dont match')
                return render(request, 'Change_pw.html', {'pw_form': post_pw_form})
        else:
            return render(request, 'Change_pw.html', {'pw_form': post_pw_form})
    return render(request, 'Change_pw.html', {'pw_form': pw_form})


# ********************************* C *************************************
# https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html Ajax
# https://realpython.com/django-and-ajax-form-submissions/ Ajax


# C1 add item to shopping cart
@login_required  # function required user login
def add_shopping_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('id', '')
        login_user_id = int(request.user.id)
        find_shop_cart = Shopping_cart.objects.filter(Product_ID_id=product_id, Cust_ID_id=login_user_id)
        if find_shop_cart.exists():
            target = find_shop_cart.get(Product_ID_id=product_id, Cust_ID_id=login_user_id)
            target.Quantity = target.Quantity + 1
            target.save()
            data = {'data': product_id}
            return JsonResponse(data)
        else:
            new_item = Shopping_cart.objects.create(Product_ID_id=product_id, Cust_ID_id=login_user_id, Quantity=1)
            new_item.save()
            data = {'data': product_id}
            return JsonResponse(data)


# C1 Redirect not login user who click add to shopping cart button
def unlogin_add_shopping_cart(request):
    messages.success(request, 'require user login to access shopping cart')
    return redirect('/b/login')


# C2 Shopping cart page
def shopping_cart(request):
    if request.user.is_authenticated:  # function required user login to access page
        info = Shopping_cart.objects.filter(Cust_ID_id=int(request.user.id)).values()
        total_amount = 0
        for e in info:
            total_amount = total_amount + (
                        float(e['Quantity']) * float(Products.objects.get(Product_ID=e['Product_ID_id']).Product_price))
            e['Product_name'] = Products.objects.get(Product_ID=e['Product_ID_id']).Product_name
            e['Product_price'] = Products.objects.get(Product_ID=e['Product_ID_id']).Product_price
            e['DisplayImage'] = Products.objects.get(Product_ID=e['Product_ID_id']).DisplayImage
        username = request.user.get_username()
        empty = True if info.first() is None else False
        context = {
            'info': info,
            'login': request.user.is_authenticated,
            'username': username,
            'total': "%.2f" % total_amount,
            'empty': empty,
        }
        return render(request, 'Shopping_cart.html', context)
    else:
        messages.success(request, 'Require user login to access Shopping cart')
        return redirect('/b/login')


# C3 Checkout item in shopping cart working
@login_required
def cart_Checkout(request, total):
    # To get all product id
    cart_product = Shopping_cart.objects.filter(Cust_ID_id=int(request.user.id)).values('Product_ID_id', 'Quantity')
    if Order.objects.last():
        new_order1 = Order.objects.create(POnumber=Order.objects.last().POnumber + 1, Total_payment=total,
                                          Cust_ID_id=int(request.user.id))
        new_order1.Order_date = datetime.datetime.now()
        new_order1.Status = 'Pending'
        new_order1.save()
        order_item_record(new_order1, cart_product)
        delete_shop_cart = Shopping_cart.objects.filter(Cust_ID_id=int(request.user.id))
        delete_shop_cart.delete()
        messages.success(request, 'All items in your shopping cart have been Checked out!')
        return redirect('/d/Purchase_detail')
    else:
        new_order = Order.objects.create(POnumber=1, Total_payment=total, Cust_ID_id=int(request.user.id))
        new_order.Order_date = datetime.datetime.now()
        new_order.Status = 'Pending'
        new_order.save()
        order_item_record(new_order, cart_product)
        delete_shop_cart = Shopping_cart.objects.filter(Cust_ID_id=int(request.user.id))
        delete_shop_cart.delete()
        messages.success(request, 'All items in your shopping cart have been Checked out!')
        return redirect('/d/Purchase_detail')


# To create Order item record
def order_item_record(new_order1, cart_product):
    for k in cart_product:
        item = Order_Items.objects.create(
            POnumber_id=new_order1.POnumber,
            Product_ID_id=k['Product_ID_id'],
            Product_price=Products.objects.get(Product_ID=k['Product_ID_id']).Product_price,
            Quantity=k['Quantity']
        )
        item.save()


# ********************************* D *************************************

# D1 Purchase tracking page
def purchase_tracking(request):
    sort_status = request.GET.get('sort_status', '')
    if request.user.is_authenticated:  # function required user login to access page
        username = request.user.get_username()
        info = Order.objects.values().filter(Cust_ID_id=request.user.id).order_by('-Order_date')  # need to check
        reset = False

        #  D2
        if sort_status != '':
            if sort_status == 'current':
                criterion1 = Q(Status="Pending")
                criterion2 = Q(Status="hold")
                info = info.filter(criterion1 | criterion2)
                reset = True
            if sort_status == 'past':
                criterion1 = Q(Status="Shipped")
                criterion2 = Q(Status="Cancelled")
                info = info.filter(criterion1 | criterion2)
                reset = True
        context = {
            'info': info,
            'login': request.user.is_authenticated,
            'username': username,
            'sort': sort_status,
            'reset': reset
        }
        return render(request, 'Purchase_tracking.html', context)
    else:
        messages.success(request, 'Require user login to view Purchase tracking page')
        return redirect('/b/login')


# D3 Purchase order page
def purchase_detail_page(request):
    if request.user.is_authenticated:  # function required user login to access page
        username = request.user.username
        info = Order.objects.filter(Cust_ID_id=request.user.id).values().order_by('-Order_date')
        for k in info:
            k['Address'] = Customer.objects.get(Cust_iD_id=request.user.id).Address
            del k['Cust_ID_id']
            k['first_name'] = request.user.first_name
            k['last_name'] = request.user.last_name
            k['username'] = username
            k['detail'] = Order_Items.objects.filter(POnumber_id=k['POnumber']).values()
            for y in k['detail']:
                y['Product_name'] = Products.objects.get(Product_ID=y['Product_ID_id']).Product_name
                del y['Product_ID_id']
                del y['id']
                cal = float(y['Product_price']) * float(y['Quantity'])
                y['subtotal'] = "%.2f" % cal
        context = {
            'info': info,
            'login': request.user.is_authenticated,
            'username': username
        }
        return render(request, 'Purchase_detail.html', context)
    else:
        messages.success(request, 'Require user login to view Purchase order')
        return redirect('/b/login')


# D Cancel ship order button
def cust_cancel_order(request, target):
    target_order = Order.objects.get(POnumber=target)
    target_order.Status = 'Cancelled'
    target_order.Cancel_date = datetime.date.today()
    target_order.Cancel_by = 'Customer'
    target_order.save()
    return redirect('/d/Purchase_detail#' + str(target))


# ********************************* F *************************************

# F1 Purchase order page
# https://stackoverflow.com/questions/12003736/django-login-required-decorator-for-a-superuser
@user_passes_test(lambda u: u.is_superuser)  # To prevent non superuser
def purchase_order(request):
    sort_process = request.GET.get('sort_order', '')
    username = request.user.get_username()
    info = Order.objects.values('POnumber', 'Order_date', 'Total_payment', 'Status', 'Cust_ID_id').order_by('-Order_date')
    reset = False
    if sort_process != '':
        if sort_process == 'pending':
            info = info.filter(Status='Pending')
            reset = True
        if sort_process == 'holding':
            info = info.filter(Status='Hold')
            reset = True
        if sort_process == 'past':
            criterion1 = Q(Status="Shipped")
            criterion2 = Q(Status="Cancelled")
            info = info.filter(criterion1 | criterion2)
            reset = True
    for k in info:
        k['first_name'] = User.objects.get(id=k['Cust_ID_id']).first_name
        k['last_name'] = User.objects.get(id=k['Cust_ID_id']).last_name
        k['username'] = User.objects.get(id=k['Cust_ID_id']).username
        del k['Cust_ID_id']
    context = {
        'login': request.user.is_authenticated,
        'username': username,
        'superuser': request.user.is_superuser,  # E1 to disable customer buttons
        'info': info,
        'sort': sort_process,
        'reset': reset
    }
    return render(request, 'Purchase_order.html', context)


# F2 Purchase processing page
@user_passes_test(lambda u: u.is_superuser)  # To prevent non superuser
def purchase_processing(request):
    search_input = request.GET.get('order_number', '')
    if request.user.is_authenticated:  # function required user login to access page
        username = request.user.username
        info = Order.objects.values().order_by('-Order_date')
        if search_input !='':
            info = Order.objects.filter(POnumber=search_input).values()
        for k in info:
            k['first_name'] = User.objects.get(id=k['Cust_ID_id']).first_name
            k['last_name'] = User.objects.get(id=k['Cust_ID_id']).last_name
            k['username'] = User.objects.get(id=k['Cust_ID_id']).username
            k['address'] = Customer.objects.get(Cust_iD=k['Cust_ID_id']).Address
            k['detail'] = Order_Items.objects.filter(POnumber_id=k['POnumber']).values()
            for y in k['detail']:
                y['Product_name'] = Products.objects.get(Product_ID=y['Product_ID_id']).Product_name
                del y['Product_ID_id']
                del y['id']
                cal = float(y['Product_price']) * float(y['Quantity'])
                y['subtotal'] = "%.2f" % cal
        context = {
            'info': info,
            'login': request.user.is_authenticated,
            'username': username,
            'superuser': request.user.is_superuser,  # E1 to disable customer buttons
            'search_input':search_input
        }
    return render(request, 'Purchase_processing.html', context)


# F3 ship order
def ship_order(request, target):
    target_order = Order.objects.get(POnumber=target)
    target_order.Status = 'Shipped'
    target_order.Ship_date = datetime.date.today()
    target_order.save()
    return redirect('/f/purchase_processing#' + str(target))


# F3 cancel order
def vendor_cancel_order(request, target):
    target_order = Order.objects.get(POnumber=target)
    target_order.Status = 'Cancelled'
    target_order.Cancel_date = datetime.date.today()
    target_order.Cancel_by = 'Vendor'
    target_order.save()
    return redirect('/f/purchase_processing#' + str(target))


# F3 hold order
def vendor_hold_order(request, target):
    target_order = Order.objects.get(POnumber=target)
    target_order.Status = 'Hold'
    target_order.save()
    return redirect('/f/purchase_processing#' + str(target))

