# Generated by Django 5.0.6 on 2025-02-16 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidones', '0004_remove_dia_bidon_15l_remove_dia_bidon_20l_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(default='Sin dirección', max_length=100),
            preserve_default=False,
        ),
    ]
