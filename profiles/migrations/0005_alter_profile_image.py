# Generated by Django 3.2.25 on 2024-10-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/default_profile_yvwtw0', upload_to='images/'),
        ),
    ]
