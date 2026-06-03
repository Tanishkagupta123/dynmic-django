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
    path('query_data/',query_data,name='query_data'),
    path('reply_query/<int:pk>',reply_query,name='reply_query'),
    path('userdashboard/query/edit/<int:pk>/',edit,name='edit'),
    path('userdashboard/query/update/<int:pk>/',update,name='update'),
    path('userdashboard/delete_query/<int:pk>/',delete_query, name='delete_query'),
    path('userdashboard/query/search/',search,name='search'),
    path('userdashboard/query/reset',reset, name='reset'),
    path('userdashboard/query/user_search',user_search, name='user_search'),
    path('userdashboard/query/user_reset',user_reset, name='user_reset'),

    
    path('delete/<int:pk>',delete,name='delete'),
    path('logout/',logout,name='logout'),


    path('admin_query_search/',admin_query_search, name='admin_query_search'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('show_attendance/', show_attendance, name='show_attendance'),
    path('my_attendance/', my_attendance, name='my_attendance'),
    path('attendance-pdf/<int:emp_id>/',attendance_pdf, name='attendance_pdf'),
    # urls.py me 'attendance_pdf' ke niche ye do lines add karo:
    path('assign-task/', assign_task, name='assign_task'),
    path('update-task-status/<int:pk>/', update_task_status, name='update_task_status'),
    path('bulk-attendance/', mark_bulk_attendance, name='bulk_attendance'),
    path('manage-teams/',manage_teams, name='manage_teams'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
