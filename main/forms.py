from django import forms
from .models import User, Package, Bookings, Destination
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Password",
        help_text="Password must be at least 8 characters long and contain both letters and numbers."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Confirm Password"
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone_number']
        widgets = {
            'password': forms.PasswordInput(),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Make last_name and phone_number required
        self.fields['last_name'].required = True
        self.fields['phone_number'].required = True
        
        # Optionally, update error messages
        self.fields['last_name'].error_messages = {'required': 'Last name is required'}
        self.fields['phone_number'].error_messages = {'required': 'Phone number is required'}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Custom password validation
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
            
            # Additional custom password requirements
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not any(char.isdigit() for char in password):
                self.add_error('password', "Password must contain at least one number.")
            if not any(char.isalpha() for char in password):
                self.add_error('password', "Password must contain at least one letter.")
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    

class LoginForm(forms.Form):
    login_identifier = forms.CharField(label="Username or Email", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class AdminLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)
    
from django import forms
from .models import Bookings

from django import forms
from .models import Bookings, Destination

class BookingForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Bookings
        fields = ['name', 'booking_date']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Make sure all fields are required
        for field in self.fields:
            self.fields[field].required = True

    # Override init to filter available packages and destinations
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)


    

class UpdateBookingForm(forms.ModelForm):
    package_cd = forms.ModelChoiceField(queryset=Package.objects.all(), label="Package")
    destination_name = forms.ModelChoiceField(queryset=Destination.objects.all(), label="Destination", required=False)

    class Meta:
        model = Bookings
        fields = ['package_cd', 'booking_date', 'destination_name']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateBookingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields['destination_name'].required = False  # Make destination optional
