# Generated by Django 5.0.7 on 2024-08-03 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0026_remove_section_content_list_content_update_in_signal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='update_in_signal',
        ),
    ]
