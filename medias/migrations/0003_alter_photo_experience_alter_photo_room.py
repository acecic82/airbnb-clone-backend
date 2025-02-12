# Generated by Django 5.0.6 on 2024-08-16 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0005_experience_category'),
        ('medias', '0002_alter_photo_file_alter_video_file'),
        ('rooms', '0006_alter_room_amenities_alter_room_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='experience',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='experiences.experience'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='rooms.room'),
        ),
    ]
