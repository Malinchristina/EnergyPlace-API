# Generated by Django 3.2.25 on 2024-10-19 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_yvwtw0', upload_to='images/'),
        ),
    ]
