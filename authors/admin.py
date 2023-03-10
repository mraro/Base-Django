from django.contrib import admin
from authors.models import Profile


# Register your models here to show in localhost\admin tab.

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    ...
