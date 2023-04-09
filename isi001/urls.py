"""isi001 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from test001 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_page),
    path('', views.home_page, name='home'),
    path('list/', views.products_list, name='rproducts'),   # read table
    path('a/', views.product_list_page, name='a'),   # A1~A5
    path('a/product/<str:target>', views.product_page, name='each_product'),   # A6~A7
    path('b/register', views.register_page, name='register'),    # B1
    path('b/login', views.login_page, name='login'),    # B2
    path('b/logout', views.logout_user, name='logout'),    # B2
    path('b/change_pw', views.change_password, name='change_password'),  # B3
    path('c/shopping_cart', views.shopping_cart, name='shopping_cart'),  # C2
    path('c/add_shopping_cart', views.add_shopping_cart, name='add_shopping_cart'),  # C1
    path('c/unlogin_add_shopping_cart', views.unlogin_add_shopping_cart, name='unlogin_add_shopping_cart'),  # c1 not login user
    re_path(r'^c/Cart_Checkout/(?P<total>\d+\.\d{2})/$', views.cart_Checkout, name='Cart_Checkout'),
    path('d/purchase_tracking', views.purchase_tracking, name='purchase_tracking'),  # D1 purchase tracking page
    path('d/Purchase_detail', views.purchase_detail_page, name='product_detail'),    # D3 purchase detail page
    path('d/Purchase_detail/cust_cancel_order/<int:target>', views.cust_cancel_order, name='cust_cancel_order'),    # D Customer cancel order
    path('f/purchase_order', views.purchase_order, name='purchase_order'),   # F1 Purchase order page
    path('f/purchase_processing', views.purchase_processing, name='purchase_processing'),   # F2 Purchase order page
    path('f/purchase_processing/ship_order/<int:target>', views.ship_order, name='ship_order'),   # F3 Ship order
    path('f/purchase_processing/cancel_order/<int:target>', views.vendor_cancel_order, name='vendor_cancel_order'),   # F Vendor cancel order
    path('f/purchase_processing/hold_order/<int:target>', views.vendor_hold_order, name='vendor_hold_order')   # F Vendor hold order
]
