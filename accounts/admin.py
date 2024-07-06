from django.contrib import admin
from .models import CustomUser, CodeEmail, ResetPasswordCode
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CodeEmail)
class CodeEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'code', 'created_at')
    search_fields = ('email', 'fullname')


@admin.register(ResetPasswordCode)
class ResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
    search_fields = ('user', 'code')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'academic_background', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fullname', 'email', 'password1', 'password2'),
        }),
    )

    list_display = ('fullname', 'email', 'academic_background', 'location', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('email',)
    search_fields = ('fullname', 'email', 'academic_background', 'location')
    ordering = ('fullname',)


admin.site.site_header = _('UniApp Administration')
admin.site.site_title = _('UniApp Admin Portal')
admin.site.index_title = _('Welcome to UniApp Admin Portal')