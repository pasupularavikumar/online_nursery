
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name ="home"),
    path("about/",views.about),
    path("shop/",views.shop),
    path("checkout/",views.checkout),
    path("news/",views.news),
    path("login/",views.loginPage),
    path("signup/",views.signUp),
    path("logout/",views.logoutUser),
    path('shop/',views.shop),
    path('singleproduct/<str:pk>',views.singleProduct),
    path('addtocart/',views.cart),
    path('cart/',views.allCart),
    path("remove-product/<int:id>",views.removeCart),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('checkpayment/', views.paymentcheckout),
    path('seller/dashboard/',views.seller_dashboard,name='seller_dashboard'),
    path('seller/users/',views.seller_users, name='seller_users'),
    path('seller/orders/',views.seller_orders, name='seller_orders'),
    path('seller/products/',views.seller_products, name='seller_products'),
    path('seller/login/',views.seller_login, name='seller_login'),
    path('seller/logout/',views.seller_logout, name='seller_logout'),
    path('seller/add/product',views.seller_add_product, name='seller_add_product'),
]


