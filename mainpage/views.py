from django.views.generic import TemplateView
from wagtail.models import Page
from blogs.models import BlogIndexPage, BlogPage


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_index = BlogIndexPage.objects.live().first()
        context["latest_posts"] = (
            BlogPage.objects.live().order_by("-date")[:3] if blog_index else []
        )
        context["blog_index_page"] = blog_index
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [
            {"title": "Home", "url": "/"},
            {"title": "About", "url": "/about/"},
        ]
        context["breadcrumb"] = breadcrumb
        return context


class HowToApplyView(TemplateView):
    template_name = "pages/how_to_apply.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [
            {"title": "Home", "url": "/"},
            {"title": "How to Apply", "url": "/how-to-apply/"},
        ]
        context["breadcrumb"] = breadcrumb
        return context


class UniPage(TemplateView):
    template_name = "pages/institution.html"


class SearchPage(TemplateView):
    template_name = "pages/search_page.html"