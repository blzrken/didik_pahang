from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import  BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Package, Destination, Bookings
from .forms import RegistrationForm, LoginForm, UpdateBookingForm

@login_required
def welcome_view(request):
    # Query the first name of the logged-in user
    user = User.objects.get(id=request.user.id)  
    first_name = user.first_name


    return render(request, 'upswelcome.html', {'first_name': first_name})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .forms import LoginForm

User = get_user_model()

def login_view(request):
    # If user is already authenticated, redirect to the appropriate page
    if request.user.is_authenticated:
        if request.user.is_superuser:  # Redirect superusers to the admin dashboard
            return redirect('admin_dashboard')
        return redirect('welcome')  # Redirect regular users to the welcome page
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_identifier = form.cleaned_data.get('login_identifier')
            password = form.cleaned_data.get('password')

            # Authenticate using email or username
            if '@' in login_identifier:
                # Authenticate using email
                try:
                    user = User.objects.get(email=login_identifier)
                except User.DoesNotExist:
                    messages.error(request, 'User with this email does not exist.')
                    return render(request, 'upslogin.html', {'form': form})
            else:
                # Authenticate using username
                try:
                    user = User.objects.get(username=login_identifier)
                except User.DoesNotExist:
                    messages.error(request, 'User with this username does not exist.')
                    return render(request, 'upslogin.html', {'form': form})

            # Now use authenticate() for the password check
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                
                # Check if the user is a superuser and redirect accordingly
                if user.is_superuser:
                    return redirect('admin_dashboard')  # Redirect superusers to the admin dashboard
                
                return redirect('welcome')  # Redirect regular users to the welcome page
            else:
                messages.error(request, 'Incorrect password.')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = LoginForm()

    return render(request, 'upslogin.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')  # Ensure only superusers can access this page

    bookings = Bookings.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete_booking':
            # Handle delete booking request
            booking_id = request.POST.get('booking_id')
            booking_to_delete = get_object_or_404(Bookings, booking_id=booking_id)
            booking_to_delete.delete()
        elif action == 'delete_user':
            # Handle delete user request
            user_id = request.POST.get('user_id')
            user_to_delete = get_object_or_404(User, id=user_id)
            user_to_delete.delete()

        return redirect('admin_dashboard')  # Refresh the page after deletion

    context = {
        'bookings': bookings,
        'users': users,
    }
    return render(request, 'upsadmin.html', context)

@login_required
def user_dashboard(request):
    bookings = Bookings.objects.filter(user=request.user).select_related('package_cd', 'destination_name')
    
    for booking in bookings:
        # Calculate total price
        package_price = booking.package_cd.price
        destination_price = booking.destination_name.price if booking.destination_name else 0
        booking.total_price = package_price + destination_price

    update_field = request.GET.get('update_field')  # Get the update_field parameter from the URL

    context = {
        'bookings': bookings,
        'user': request.user,
        'update_field': update_field,  # Add this to the context
    }
    return render(request, 'upsuser.html', context)

# Registration view

from django.contrib.auth.hashers import make_password
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'upsregister.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')


def package_view(request):
    # Fetch the packages
    packages = Package.objects.all()
    
    user_phone_number = request.user.phone_number if request.user.is_authenticated else ''

    context = {
        'packages': packages,
        'user_phone_number': user_phone_number,
    }
    return render(request, 'upspackages.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm
from .models import Package, Bookings

@login_required
def book_package(request, package_cd):
    package = get_object_or_404(Package, package_cd=package_cd)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        print("Form data:", request.POST)  # Debug print
        if form.is_valid():
            booking = form.save(commit=False)
            booking.package_cd = package
            booking.user = request.user
            booking.price = package.price

            # Generate a sequential booking ID
            last_booking = Bookings.objects.all().order_by('booking_id').last()
            if last_booking:
                last_id = int(last_booking.booking_id[1:])
                new_id = f"B{last_id + 1:03d}"
            else:
                new_id = "B001"

            booking.booking_id = new_id
            booking.save()

            print(f"Booking saved with ID: {booking.booking_id}")  # Debug print
            print(f"Redirecting to: {reverse('booking_confirmation', args=[booking.booking_id])}")  # Debug print
            return redirect('booking_confirmation', booking_id=booking.booking_id)
        else:
            print("Form errors:", form.errors)  # Debug print
    else:
        form = BookingForm()

    context = {
        'form': form,
        'package': package,
    }
    return render(request, 'upspackage-book.html', context)


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Bookings, booking_id=booking_id)

    context = {
        'booking': booking
    }
    return render(request, 'upsbook-confirm.html', context)

@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Bookings, booking_id=booking_id, user=request.user)

    if request.method == 'POST':
        form = UpdateBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking updated successfully!')
            return redirect('user_dashboard')
    else:
        form = UpdateBookingForm(instance=booking)

    return render(request, 'update_booking.html', {
        'form': form,
        'booking': booking,
    })

from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Bookings, booking_id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking deleted successfully!')
    else:
        messages.error(request, 'Invalid request method for deleting booking.')
    
    return HttpResponseRedirect(reverse('user_dashboard'))

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        update_field = request.POST.get('update_field')
        
        if update_field == 'name':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
        elif update_field == 'username':
            user.username = request.POST.get('username', user.username)
        elif update_field == 'phone_number':
            user.phone_number = request.POST.get('phone_number', user.phone_number)
        elif update_field == 'password':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
            else:
                messages.error(request, 'Passwords do not match or are empty.', extra_tags='profile_update')
                return redirect('user_dashboard')

        try:
            user.save()
            messages.success(request, f'{update_field.capitalize()} updated successfully.', extra_tags='profile_update')
        except Exception as e:
            messages.error(request, f'Error updating {update_field}: {str(e)}', extra_tags='profile_update')

    return redirect('user_dashboard')

@login_required
def user_update(request):
    update_field = request.GET.get('update_field')
    context = {
        'user': request.user,
        'update_field': update_field,
    }
    return render(request, 'upsuser-update.html', context)


@login_required
def upsdestination(request):
    destinations = Destination.objects.all()
    user_bookings = Bookings.objects.filter(user=request.user).select_related('package_cd')
    
    # Create a dictionary of booking IDs and their destination names
    bookings_with_destinations = {
        booking.booking_id: booking.destination_name.destination_name if booking.destination_name else None
        for booking in user_bookings
    }
    
    context = {
        'destinations': destinations,
        'user_bookings': user_bookings,
        'bookings_with_destinations': bookings_with_destinations,
    }
    return render(request, 'upsdestination.html', context)


@login_required
def add_destination_to_booking(request):
    if request.method == 'POST':
        destination_name = request.POST.get('destination_name')
        booking_id = request.POST.get('booking_id')
        user = request.user

        try:
            booking = Bookings.objects.get(booking_id=booking_id, user=user)
            
            if booking.destination_name:
                messages.error(request, f'Booking {booking_id} already has a destination: {booking.destination_name.destination_name}', extra_tags='destination')
            else:
                destination = Destination.objects.get(destination_name=destination_name)
                booking.destination_name = destination
                booking.save()
                messages.success(request, f'{destination_name} added to booking {booking_id} successfully!', extra_tags='destination')
        except Bookings.DoesNotExist:
            messages.error(request, 'Selected booking does not exist or does not belong to you.', extra_tags='destination')
        except Destination.DoesNotExist:
            messages.error(request, 'Selected destination does not exist.', extra_tags='destination')

    return redirect('upsdestination')

def about_view(request):
    return render(request, 'upsabout.html')
