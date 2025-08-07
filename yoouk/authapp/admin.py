from django.contrib import admin
from .models import User

# Register your models here.
class CustomUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'is_staff', 'is_active')

admin.site.register(User, CustomUser)
