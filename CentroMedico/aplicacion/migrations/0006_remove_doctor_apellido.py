# Generated by Django 5.0.1 on 2024-02-28 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0005_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='apellido',
        ),
    ]