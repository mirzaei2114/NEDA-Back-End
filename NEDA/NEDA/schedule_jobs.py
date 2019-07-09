from django.utils import timezone
from datetime import timedelta, datetime
from django_cron import CronJobBase, Schedule

from TimeReservation.models import WorkingHour, DAYS_PER, AppointmentTime


class CreateNew(CronJobBase):
    RUN_AT_TIMES = ['00:00']
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'NEDA.CreateNewAppointments'    # a unique code

    def do(self):
        now = timezone.now()
        print(now, DAYS_PER[now.weekday() + 2])
        working_hours = WorkingHour.objects.filter(day=DAYS_PER[now.weekday() + 2])
        for working_hour in working_hours:
            appointments = []
            try:
                start = datetime(now.year, now.month, now.day,
                                 working_hour.start.hour, working_hour.start.minute) + timedelta(days=14)
                end = datetime(now.year, now.month, now.day,
                               working_hour.end.hour, working_hour.end.minute) + timedelta(days=14)
                period = working_hour.period
                while start + timedelta(minutes=period) <= end:
                    data = {'date_time': start, 'reservation_date_time': None, 'has_reserved': False,
                            'price': working_hour.price, 'doctor': working_hour.doctor, 'patient': None, 'clinic': working_hour.clinic,
                            'hospital': working_hour.hospital}
                    appointment_time = AppointmentTime.objects.create(**data)
                    appointments.append(appointment_time)
                    start += timedelta(minutes=period)
                    appointment_time.save()
                print('Success on working hour: ' + str(working_hour.id))
            except Exception as e:
                for appointment in appointments:
                    if appointment:
                        appointment.delete()
                print('Failed on working hour: ' + str(working_hour.id) + str(e.args))
