# Generated by Django 5.0.6 on 2024-06-06 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_blogpage_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
