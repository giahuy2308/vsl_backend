# Generated by Django 5.0.7 on 2024-08-30 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0041_alter_section_component_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='component_quantity',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
