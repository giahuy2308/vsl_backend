# Generated by Django 5.0.7 on 2024-08-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0025_section_content_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='content_list',
        ),
        migrations.AddField(
            model_name='content',
            name='update_in_signal',
            field=models.BooleanField(default=False),
        ),
    ]
