# Generated by Django 5.1.6 on 2025-03-14 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_alter_card_image'),
        ('qrgenerator', '0009_merge_0007_website_date_0008_website_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cards.card'),
        ),
    ]
