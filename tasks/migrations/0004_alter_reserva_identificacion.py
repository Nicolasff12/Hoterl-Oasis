# Generated by Django 5.1.1 on 2024-11-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_reserva_adultos_alter_reserva_habitacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='identificacion',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
