# Generated by Django 5.0.7 on 2024-08-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0040_alter_animation_no_alter_content_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='component_quantity',
            field=models.BigIntegerField(default=0),
        ),
    ]
