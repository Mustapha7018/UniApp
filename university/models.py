from django.db import models
from django.utils.translation import gettext_lazy as _


class UniversityType(models.TextChoices):
    PUBLIC = 'PUB', _('Public')
    PRIVATE = 'PRI', _('Private')

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='university_logos/')
    type = models.CharField(
        max_length=10,
        choices=UniversityType.choices,
        default=UniversityType.PUBLIC
    )
    card_image = models.ImageField(upload_to='university_cards/')
    banner = models.ImageField(upload_to='university_banners/')
    map_location = models.URLField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='universities')
    
    # Social media links
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"

