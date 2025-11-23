from django.urls import path, include
from . import views

urlpatterns = [
    path('driver/login/', views.driver_login, name='driver_login'),
    path('rider/login/', views.rider_login, name='rider_login'),
    path('driver/signup/', views.driver_signup, name='driver_signup'),
    path('rider/signup/', views.rider_signup, name='rider_signup'),
    path('set-user-type/<str:user_type>/', views.set_user_type, name='set_user_type'),
    path('', include('allauth.urls')),
    path('social/start/<str:role>/', views.start_social_login, name='start_social_login'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('verification/', views.verification, name='verification'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
]