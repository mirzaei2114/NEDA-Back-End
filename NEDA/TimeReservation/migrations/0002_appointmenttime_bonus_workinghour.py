# Generated by Django 2.2.2 on 2019-06-13 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_auto_20190612_2123'),
        ('TimeReservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingHour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.CharField(choices=[('شنبه', 'شنبه'), ('یکشنبه', 'یکشنبه'), ('دوشنبه', 'دوشنبه'), ('سه شنبه', 'سه شنبه'), ('چهارشنبه', 'چهارشنبه'), ('پنج شنبه', 'پنج شنبه'), ('جمعه', 'جمعه')], max_length=8)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('off_percent', models.IntegerField()),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Doctor')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('reserved', models.BooleanField(default=False)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Doctor')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Patient')),
            ],
        ),
    ]
