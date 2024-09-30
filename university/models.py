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
    abbreviation = models.CharField(max_length=10, blank=True, null=True)  # e.g., "UG"
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='university_logos/')
    type = models.CharField(
        max_length=10,
        choices=UniversityType.choices,
        default=UniversityType.PUBLIC
    )
    card_image = models.ImageField(upload_to='university_cards/')
    banner = models.ImageField(upload_to='university_banners/', blank=True, null=True)
    map_location = models.URLField(help_text="URL for the embedded map (e.g., Google Maps)")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='universities')
    
    # Contact Information
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    address_line3 = models.CharField(max_length=255, blank=True)
    
    # Social media links
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
        
    # Academic Program Links
    graduate_program_url = models.URLField(blank=True)
    undergraduate_program_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"

class AcademicProgram(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('UG', 'Undergraduate'),
        ('GR', 'Graduate'),
    ]

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='academic_programs')
    program_type = models.CharField(max_length=2, choices=PROGRAM_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.get_program_type_display()} - {self.name}"

class GeneralRequirement(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='general_requirements')
    requirement = models.TextField()

    def __str__(self):
        return f"Requirement for {self.university.name}"

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('AD', 'Additional Info'),
        ('UL', 'Useful Links'),
        ('DS', 'Discover'),
    ]

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=2, choices=RESOURCE_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f"{self.get_resource_type_display()} - {self.title}"


class AboutParagraph(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='about_paragraphs')
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Paragraph {self.order} for {self.university.name}"