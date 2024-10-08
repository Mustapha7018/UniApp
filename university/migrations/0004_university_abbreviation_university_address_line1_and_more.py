# Generated by Django 5.0.6 on 2024-09-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("university", "0003_location_university_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="university",
            name="abbreviation",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="university",
            name="address_line1",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="university",
            name="address_line2",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="university",
            name="address_line3",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="university",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="university",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="university",
            name="graduate_program_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="university",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="university",
            name="undergraduate_program_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="university",
            name="banner",
            field=models.ImageField(
                blank=True, null=True, upload_to="university_banners/"
            ),
        ),
    ]
