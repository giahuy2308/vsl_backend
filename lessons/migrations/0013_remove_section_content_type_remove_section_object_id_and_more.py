# Generated by Django 5.0.7 on 2024-07-20 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0012_remove_animation_section_remove_content_section_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='section',
            name='object_id',
        ),
        migrations.AddField(
            model_name='animation',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='animations', to='lessons.section'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='lessons.section'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='lessons.section'),
            preserve_default=False,
        ),
    ]
