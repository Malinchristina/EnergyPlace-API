# Generated by Django 4.2 on 2024-11-09 08:46

from django.db import migrations, models

def set_default_category(apps, schema_editor):
    # Get the Post and Category models
    Post = apps.get_model('posts', 'Post')
    Category = apps.get_model('categories', 'Category')
    
    # Get or create the "Other" category
    other_category, created = Category.objects.get_or_create(name='other')
    
    # Set "Other" category for posts without a category
    Post.objects.filter(category__isnull=True).update(category=other_category)

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_category'),
    ]

    operations = [
        migrations.RunPython(set_default_category),
    ]


