# Generated by Django 5.1.5 on 2025-03-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrgenerator', '0006_remove_website_latitude_remove_website_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='location',
        ),
        migrations.AddField(
            model_name='website',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='website',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
