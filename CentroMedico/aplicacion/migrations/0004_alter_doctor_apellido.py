# Generated by Django 5.0.1 on 2024-02-27 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_doctor_apellido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='apellido',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]