# Generated by Django 5.1.5 on 2025-02-22 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_alter_card_card_desc_alter_card_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='value',
            field=models.IntegerField(default=0, verbose_name='Card Value'),
        ),
    ]
