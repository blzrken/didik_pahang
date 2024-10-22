"""
URL configuration for didik_pahang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Redirect to login view for the home URL
    path('jelajahdidikpahang/', views.welcome_view, name="welcome"),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('packages/', views.package_view, name='package'),
    path('package-booking/<str:package_cd>/', views.book_package, name='book_package'),
    path('booking-confirmation/<str:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('user-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('booking/<str:booking_id>/update/', views.update_booking, name='update_booking'),
    path('booking/<str:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('destinations/', views.upsdestination, name='upsdestination'),
    path('add-destination/', views.add_destination_to_booking, name='add_destination_to_booking'),
    path('about/', views.about_view, name='about'),
]

