# Generated by Django 5.0.6 on 2024-07-30 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_customuser_aggregate_customuser_course_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="course",
        ),
    ]
