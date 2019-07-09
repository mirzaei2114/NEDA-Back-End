# Generated by Django 2.2.3 on 2019-07-09 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('province', models.CharField(choices=[('آذربایجان شرقی', 'آذربایجان شرقی'), ('آذربایجان غربی', 'آذربایجان غربی'), ('اردبیل', 'اردبیل'), ('اردبیل', 'اردبیل'), ('اصفهان', 'اصفهان'), ('البرز', 'البرز'), ('ایلام', 'ایلام'), ('بوشهر', 'بوشهر'), ('تهران', 'تهران'), ('چهارمحال و بختیاری', 'چهارمحال و بختیاری'), ('خراسان جنوبی', 'خراسان جنوبی'), ('خراسان رضوی', 'خراسان رضوی'), ('خراسان شمالی', 'خراسان شمالی'), ('خوزستان', 'خوزستان'), ('زنجان', 'زنجان'), ('سمنان', 'سمنان'), ('سیستان و بلوچستان', 'سیستان و بلوچستان'), ('فارس', 'فارس'), ('قزوین', 'قزوین'), ('قم', 'قم'), ('کردستان', 'کردستان'), ('کرمان', 'کرمان'), ('کرمانشاه', 'کرمانشاه'), ('کهگیلویه و بویراحمد', 'کهگیلویه و بویراحمد'), ('گلستان', 'گلستان'), ('گیلان', 'گیلان'), ('لرستان', 'لرستان'), ('مازندران', 'مازندران'), ('مرکزی', 'مرکزی'), ('هرمزگان', 'هرمزگان'), ('همدان', 'همدان'), ('یزد', 'یزد')], max_length=19)),
                ('phone_number', models.CharField(max_length=8)),
                ('address', models.CharField(max_length=512)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_clinics', to='Accounts.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingHour',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.CharField(choices=[('شنبه', 'شنبه'), ('یکشنبه', 'یکشنبه'), ('دوشنبه', 'دوشنبه'), ('سه شنبه', 'سه شنبه'), ('چهارشنبه', 'چهارشنبه'), ('پنج شنبه', 'پنج شنبه'), ('جمعه', 'جمعه')], max_length=8)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('period', models.IntegerField(help_text='in minutes')),
                ('price', models.IntegerField()),
                ('clinic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinic_working_hours', to='TimeReservation.Clinic')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_working_hours', to='Accounts.Doctor')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_working_hours', to='Accounts.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Doctor')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Accounts.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('reservation_date_time', models.DateTimeField(null=True)),
                ('has_reserved', models.BooleanField(default=False)),
                ('visitation_time', models.TimeField(default=None, null=True)),
                ('visiting', models.BooleanField(default=False)),
                ('visited', models.BooleanField(default=False)),
                ('price', models.IntegerField()),
                ('bonus_amount', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('clinic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinic_appointment_times', to='TimeReservation.Clinic')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointment_times', to='Accounts.Doctor')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_appointment_times', to='Accounts.Hospital')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointment_times', to='Accounts.Patient')),
            ],
        ),
    ]
