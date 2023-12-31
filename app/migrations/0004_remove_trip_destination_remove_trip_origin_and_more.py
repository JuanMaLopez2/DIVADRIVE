# Generated by Django 4.2.7 on 2023-11-12 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_trip_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='origin',
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_lat',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_lon',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_lat',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_lon',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
    ]
