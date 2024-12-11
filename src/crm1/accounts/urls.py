from django.urls import path
from . import views
urlpatterns = [
    path('loginpage/', views.loginPage, name='loginpage'),
    path('registerpage/', views.registerPage, name='registerpage'),
    path('logoutpage/', views.logoutPage, name='logoutpage'),
    path('', views.home, name='dashboard'),
    path('products/', views.products, name='products'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('createorder/', views.createOrder, name='createorder'),
    path('updateorder/<int:pk>/', views.updateOrder, name='updateorder'),
    path('deleteorder/<int:pk>/', views.deleteOrder, name='deleteorder'),
    path('userpage/', views.userPage, name='userpage'),
    path('customprofile/', views.customerProfile, name='customprofile'),
]