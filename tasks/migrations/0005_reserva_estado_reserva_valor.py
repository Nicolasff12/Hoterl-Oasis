# Generated by Django 4.2.16 on 2024-11-25 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_reserva_identificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='estado',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserva',
            name='valor',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]