# Generated by Django 5.0.7 on 2024-07-24 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0020_assignment_mark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='mark',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='examination',
            old_name='total_mark',
            new_name='total_score',
        ),
    ]
