from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomeView
from wagtail.models import Page
from blogs.models import BlogIndexPage, BlogPage
from django.utils import timezone


class HomePageTests(TestCase):
    def setUp(self):
        Page.objects.filter(slug="home").delete()

        root = Page.objects.get(id=1)
        home_page = Page(title="Home", slug="home")
        root.add_child(instance=home_page)
        home_page.save()

        # Create a BlogIndexPage and some BlogPages
        self.blog_index = BlogIndexPage(title="Blog", slug="blog")
        home_page.add_child(instance=self.blog_index)
        self.blog_index.save()

        for i in range(3):
            blog_page = BlogPage(
                title=f"Blog Post {i+1}",
                date=timezone.now(),
                slug=f"blog-post-{i+1}",
                body="This is a test blog post.",
                intro="This is the intro for the blog post.",
            )
            self.blog_index.add_child(instance=blog_page)
            blog_page.save()

    def test_home_view_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolve(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)
