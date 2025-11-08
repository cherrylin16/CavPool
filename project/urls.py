"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("ridesharing/", include("ridesharing.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("", include("dashboard.urls")),
    path("", include("driver_profile.urls")),
    path("", include("rider_profile.urls")),
    path("messages/", include("messaging.urls")),
    path('google29704b4949bc33ee.html', TemplateView.as_view(template_name='google1234567890abcdef.html')),
]
