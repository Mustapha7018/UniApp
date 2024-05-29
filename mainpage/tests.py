from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomeView  

class HomePageTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolve(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)

