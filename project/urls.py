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
    path('dashboard/add_emp/',add_emp,name='add_emp'),
    path('dashboard/add_dep/',add_dep,name='add_dep'),
    path('dashboard/all_dep/',all_dep,name='all_dep'),
    path('dashboard/all_emp/',all_emp,name='all_emp'),
    path('show_query/',show_query,name='show_query'),
    path('dashboard/profile/',profile,name='profile'),
    path('dashboard/query',query,name='query'),
    path('dashboard/query_status',query_status,name='query_status'),
    path('dashboard/all_query',all_query,name='all_query'),
    path('userdashboard/',userdashboard,name='userdashboard'),

    path('delete/<int:pk>',delete,name='delete'),
    path('logout/',logout,name='logout')




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
