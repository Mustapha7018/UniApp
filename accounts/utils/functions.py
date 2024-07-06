import random
from datetime import timedelta
from django.utils import timezone


def generate_activation_code():
    return int("".join([str(random.randint(1, 9)) for _ in range(6)]))


def is_expired(created_at, expiration_time=timedelta(minutes=15)):
    return timezone.now() > (created_at + expiration_time)


