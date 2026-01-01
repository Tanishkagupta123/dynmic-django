"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing,name='landing'),
    path('registration/',registration,name='registration'),
    # path('regiterdata/',regiterdata,name='regiterdata'),
    path('show_data/',show_data,name="show_data"),
    path('login/',login,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logout/',logout,name='logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
