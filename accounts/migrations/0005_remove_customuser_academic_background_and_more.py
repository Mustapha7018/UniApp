# Generated by Django 5.0.6 on 2024-07-30 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_remove_customuser_course"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="academic_background",
        ),
        migrations.AddField(
            model_name="customuser",
            name="course",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
