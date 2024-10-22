from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

# Custom UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, username, phone_number=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Ensures the password is hashed
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, phone_number, password, **extra_fields)

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default='User')  

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='main_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='main_user_permissions',
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_staff and self.is_superuser:
            self.role = 'Staff'
        else:
            self.role = 'User'
        super().save(*args, **kwargs)

# Package model
class Package(models.Model):
    package_cd = models.CharField(max_length=10, primary_key=True)  
    package_desc = models.TextField()  
    price = models.IntegerField() 

    def display_price(self):
        """Return price with RM prefix."""
        return f"RM{self.price:.2f}"

# Destination model
class Destination(models.Model):
    destination_name = models.CharField(max_length=100, primary_key=True)
    price = models.IntegerField()
    tags = models.ManyToManyField('Tag', related_name='destinations', blank=True)

    def __str__(self):
        return self.destination_name
    
    def display_price(self):
        """Return price with RM prefix."""
        return f"RM{self.price:.2f}"

    def get_tags(self):
        """Return a list of tag names for this destination."""
        return [tag.name for tag in self.tags.all()]

# Bookings model
class Bookings(models.Model):
    booking_id = models.CharField(max_length=10, primary_key=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    package_cd = models.ForeignKey(Package, on_delete=models.CASCADE)  
    destination_name = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)  
    name = models.CharField(max_length=100)
    booking_date = models.DateField()
    price = models.IntegerField() 

    def __str__(self):
        return f"Booking {self.booking_id} by {self.name} - Price: RM {self.price}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
