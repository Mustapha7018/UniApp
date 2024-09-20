from django.contrib import admin
from .models import University

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'type')
    list_filter = ('type', 'region')
    search_fields = ('name', 'city', 'region')

# admin.site.register(University, UniversityAdmin)

