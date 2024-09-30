from django.urls import path
from .views import FeedbackView

urlpatterns = [
    path("submit-feedback/", FeedbackView.as_view(), name="submit_feedback"),
]
