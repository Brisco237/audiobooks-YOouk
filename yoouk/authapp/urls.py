from django.urls import path   
from authapp import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('', views.logout_user, name='logout_user'),
    
]