# Generated by Django 5.0.6 on 2024-07-07 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_alter_perk_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perk',
            name='details',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='perk',
            name='explanation',
            field=models.TextField(blank=True, default=''),
        ),
    ]
