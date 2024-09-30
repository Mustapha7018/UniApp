from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from .models import CodeEmail

@shared_task
def delete_unverified_users():
    # Set time threshold
    time_threshold = timezone.now() - timezone.timedelta(minutes=30)
    
    # Filter and delete unverified users older than 30 minutes
    deleted_count, _ = CodeEmail.objects.filter(created_at__lte=time_threshold).delete()
    return f"Deleted {deleted_count} unverified users."