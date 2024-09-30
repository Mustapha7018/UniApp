from django.http import JsonResponse
from django.views import View
from .models import Feedback

# Create your views here.


class FeedbackView(View):
    def post(self, request, *args, **kwargs):
        feedback_value = request.POST.get("feedback")
        page = request.POST.get("page")
        feedback = Feedback(feedback=feedback_value, page=page)
        feedback.save()
        return JsonResponse({"message": "Feedback recorded"})

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=400
        )
