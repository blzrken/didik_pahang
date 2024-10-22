from django.contrib import admin

# Register your models here.

from .models import User, Package, Destination, Bookings, Tag

admin.site.register(User)
admin.site.register(Package)
admin.site.register(Destination)
admin.site.register(Bookings)
admin.site.register(Tag)
