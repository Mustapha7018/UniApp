from django.contrib import admin
from .models import University, Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location')
    list_filter = ('type', 'location')
    search_fields = ('name', 'city', 'region')

