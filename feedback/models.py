from django.db import models


class Feedback(models.Model):
    PAGE_CHOICES = [
        ("search page", "Search Page"),
        ("about", "About"),
        ("how to apply", "Resources"),
        ("uni page", "Uni Page"),
    ]

    FEEDBACK_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    page = models.CharField(max_length=100, choices=PAGE_CHOICES)
    feedback = models.CharField(max_length=3, choices=FEEDBACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback} on {self.page}"
