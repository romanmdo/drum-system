# Generated by Django 5.0.6 on 2025-02-17 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bidones', '0006_rename_bidones_15l_dia_bidones_12l_dia_alquila_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dia',
            old_name='bidones_12L',
            new_name='bidones_15L',
        ),
    ]
