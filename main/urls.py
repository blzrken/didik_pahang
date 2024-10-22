from django.urls import path, include
from .views import register_view, login_view, package_view, book_package, user_dashboard, update_profile, upsdestination, add_destination_to_booking, booking_confirmation, about_view

urlpatterns = [
    path('', include('login.urls')),  # Include login URLs
    path('welcomepage/', include('welcome.urls')),  # Include welcome URLs
    path('register/', register_view, name='register'),  # Route for registration
    path('login/', login_view, name='login'),  # Route for login
    path('packages/', package_view, name='package'), # Route for package
    path('package-booking/<str:package_cd>/', book_package, name='book_package'), 
    path('booking-confirmation/<str:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('update-profile/', update_profile, name='update_profile'),
    path('destinations/', upsdestination, name='upsdestination'),
    path('add-destination/', add_destination_to_booking, name='add_destination_to_booking'),
    path('about/', about_view, name='about'),
]
