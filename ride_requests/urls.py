from django.urls import path
from . import views

app_name = 'ride_requests'

urlpatterns = [
    path('request/<int:post_id>/', views.request_ride, name='request_ride'),
    path('manage/<int:post_id>/', views.manage_requests, name='manage_requests'),
    path('update/<int:request_id>/', views.update_request_status, name='update_request_status'),
    path('cancel/<int:request_id>/', views.cancel_request, name='cancel_request'),
]