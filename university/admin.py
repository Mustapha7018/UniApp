from django.contrib import admin
from .models import University, Location, AcademicProgram, GeneralRequirement, Resource, AboutParagraph

class AcademicProgramInline(admin.TabularInline):
    model = AcademicProgram
    extra = 1

class GeneralRequirementInline(admin.TabularInline):
    model = GeneralRequirement
    extra = 1

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class AboutParagraphInline(admin.TabularInline):
    model = AboutParagraph
    extra = 1
    fields = ('content', 'order')
    ordering = ('order',)



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'abbreviation')
    list_filter = ('type', 'location')
    search_fields = ('name', 'city', 'region', 'abbreviation')
    fieldsets = (
        ('General Info', {
            'fields': ('name', 'abbreviation', 'type', 'location', 'city', 'region')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address_line1', 'address_line2', 'address_line3')
        }),
        ('Media', {
            'fields': ('logo', 'card_image', 'banner', 'map_location')
        }),
        ('Social Media Links', {
            'fields': ('twitter', 'facebook', 'instagram', 'linkedin', 'website_url')
        }),
        ('Academic Programs', {
            'fields': ('graduate_program_url', 'undergraduate_program_url')
        }),
    )

    inlines = [
        AcademicProgramInline,
        GeneralRequirementInline,
        ResourceInline,
        AboutParagraphInline
    ]

