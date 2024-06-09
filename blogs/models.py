from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.images.models import Image

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['BlogPage']

    template = "blog/blog_index_page.html"

    def get_latest_posts(self):
        return BlogPage.objects.live().order_by('-date')

    def get_context(self, request):
        context = super().get_context(request)
        context['posts'] = self.get_latest_posts()
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    author = models.CharField(max_length=250, blank=True, null=True)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_description = models.CharField(max_length=255, blank=True, null=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('featured_image'),  
            FieldPanel('image_description'),
        ], heading="Blog Content"),
    ]

    template = "blog/blog_page.html"
    parent_page_types = ['BlogIndexPage']

    def get_recommended_posts(self):
        return BlogPage.objects.sibling_of(self).live().exclude(id=self.id).order_by('-date')[:3]


    def get_context(self, request):
        context = super().get_context(request)
        context['recommended_posts'] = self.get_recommended_posts()
        return context
