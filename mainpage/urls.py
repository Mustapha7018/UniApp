from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("how-to-apply/", HowToApplyView.as_view(), name="how-to-apply"),
    path("uni/", UniPage.as_view(), name="ug-site"),
]
