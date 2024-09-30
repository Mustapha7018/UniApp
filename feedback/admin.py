from django.contrib import admin
from .models import Feedback


# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("page", "feedback", "created_at")
    list_filter = ("created_at", "feedback")


admin.site.register(Feedback, FeedbackAdmin)
