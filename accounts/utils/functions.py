import random
from django.utils import timezone


def generate_activation_code():
    return int("".join([str(random.randint(1, 9)) for _ in range(6)]))


def is_expired(updated_time):
    time_difference = timezone.now() - updated_time
    return (time_difference.seconds // 3600) >= 24


