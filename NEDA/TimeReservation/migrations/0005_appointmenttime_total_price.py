# Generated by Django 2.2.2 on 2019-07-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeReservation', '0004_auto_20190708_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmenttime',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
