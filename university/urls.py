from django.urls import path
from .views import *

urlpatterns = [
    path('search-page/', UniversityListView.as_view(), name='search-page'),
    path('university_detail/<int:pk>/', UniversityDetailView.as_view(), name='university-detail'),
]
