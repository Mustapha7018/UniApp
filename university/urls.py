from django.urls import path
from .views import *

urlpatterns = [
    path("search-page/", UniversityListView.as_view(), name="search-page"),
    path("toggle-favorite/", ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path(
        "university_detail/<int:pk>/",
        UniversityDetailView.as_view(),
        name="university-detail",
    ),
]
