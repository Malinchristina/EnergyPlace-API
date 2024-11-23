# Generated by Django 4.2 on 2024-11-11 20:10

from django.db import migrations

def create_default_location(apps, schema_editor):
    Location = apps.get_model("locations", "Location")
    Location.objects.get_or_create(name="Unknown", country="ZZ")  # ZZ represent an unspecified country

class Migration(migrations.Migration):
    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_location),
    ]