# Generated by Django 4.2 on 2024-11-24 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='../default_post_lskfrc', upload_to='images/'),
        ),
    ]