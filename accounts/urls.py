from django.urls import path
from accounts import views

urlpatterns = [
    path('login/',views.loginPage, name='login'),
    path('register/',views.registerPage, name='register'),
    path('logout/', views.logoutUser, name="logout"),

    path('',views.home, name='home'),
    path('user/',views.userPage, name='user-page'),
    path('profile/',views.userProfile, name='profile'),
    path('products/',views.products, name='products'),
    path('customer/<str:pk>/',views.customer, name='customer'),

    path('create_customer/',views.createCustomer, name='create_customer'),
    path('create_order/<str:pk>/',views.createOrder, name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder, name='delete_order'),
    path('view_tag/<str:pk>/',views.viewTag, name='view_tag')

]