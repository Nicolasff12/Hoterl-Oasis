# Generated by Django 5.1.1 on 2024-11-24 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='menores',
            field=models.IntegerField(default=0),
        ),
    ]