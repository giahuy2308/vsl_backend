# Generated by Django 5.0.7 on 2024-07-21 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_notification_from_notification_content_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='content_type',
            new_name='From',
        ),
    ]
