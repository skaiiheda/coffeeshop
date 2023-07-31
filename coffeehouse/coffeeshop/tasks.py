# from celery import shared_task
# from django.db.models import Sum
# from datetime import timedelta, datetime
# from .models import Employee, Shift, Attendance
#
# @shared_task
# def generate_report():
#     # Получаем дату воскресенья текущей недели
#     sunday = datetime.now().date() - timedelta(days=datetime.now().weekday() + 1)
#
#     # Получаем список сотрудников и их посещаемость за текущую неделю
#     employees = Employee.objects.all()
#     shifts = Shift.objects.filter(day__gte=sunday)
#
#     # Формируем отчет для каждого сотрудника
#     for employee in employees:
#         # Получаем количество отработанных часов и опозданий за неделю
#         total_hours = attendance.filter(employee=employee).aggregate(Sum('end_time') - Sum('start_time'))['end_time__sum'] or timedelta()
#         late_minutes = attendance.filter(employee=employee, start_time__gt=datetime.combine(sunday, employee.start_time)).aggregate(Sum('start_time' - datetime.combine(sunday, employee.start_time)))['start_time__sum'] or timedelta()
#
#         # Получаем количество уходов раньше смены за неделю
#         early_minutes = timedelta()
#         for day in range(0, 7):
#             end_of_shift = datetime.combine(sunday + timedelta(days=day), employee.end_time)
#             early_minutes += attendance.filter(employee=employee, date=sunday + timedelta(days=day), end_time__lt=end_of_shift).aggregate(Sum(end_of_shift - 'end_time'))['end_time__sum'] or timedelta()
#
#         # Вычисляем заработную плату за неделю
#         total_pay = total_hours.seconds / 3600 * employee.hourly_rate
#
#         # Сохраняем отчет в базу данных
#         report = Report(employee=employee, week_start=sunday, week_end=sunday + timedelta(days=6), total_hours=total_hours, late_minutes=late_minutes, early_minutes=early_minutes, total_pay=total_pay)
#         report.save()

import datetime
from celery import shared_task
from django.utils import timezone
from .models import Employee, Attendance, Shift


@shared_task
def generate_weekly_report():
    # Получаем текущую неделю
    today = timezone.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    selected_date = start_of_week + datetime.timedelta(days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(selected_day.lower()))

    # Получаем всех сотрудников
    employees = Employee.objects.all()

    # Формируем отчет для каждого сотрудника
    for employee in employees:
        shifts = Shift.objects.filter(employee=employee, day__gte=start_of_week, day__lte=end_of_week)

        # Рассчитываем часы, опоздания, ранние уходы и заработную плату для каждой смены
        total_hours = 0
        total_late_arrivals = 0
        total_early_departures = 0
        total_earnings = 0

        for shift in shifts:
            pass
            # ... рассчет часов и заработной платы для смены ...

        # Сохраняем отчет в базу данных
        # Здесь предполагается, что у модели Employee есть поле для хранения отчета,
        # куда можно сохранить вычисленные значения для каждого сотрудника за неделю.
        employee.weekly_report = {
            'total_hours': total_hours,
            'total_late_arrivals': total_late_arrivals,
            'total_early_departures': total_early_departures,
            'total_earnings': total_earnings,
        }
        employee.save()
        print(employee.weekly_report)



# tasks.py

# from celery import shared_task
# import datetime
# from .models import Employee, Shift, Attendance
#
#
# @shared_task
# def generate_weekly_report_for_day(selected_day):
#     # Получаем текущую дату и время
#     current_date = datetime.datetime.now()
#
#     # Находим дату воскресенья текущей недели
#     sunday = current_date + datetime.timedelta(days=(6 - current_date.weekday()))
#
#     # Находим дату понедельника текущей недели
#     monday = sunday - datetime.timedelta(days=6)
#
#     # Получаем дату выбранного дня недели
#     selected_date = monday + datetime.timedelta(days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(selected_day.lower()))
#
#     # Получаем все смены за выбранный день недели
#     shifts = Shift.objects.filter(day=selected_day.lower())
#     attendances = Attendance.objects.all()
#
#     # Инициализируем словарь для хранения данных отчета
#     report_data = {}
#
#     # Итерируемся по каждой смене и считаем информацию для отчета
#     for shift in shifts:
#         employee = shift.employee
#         total_work_hours = (shift.end_time - shift.start_time).seconds / 3600  # Время работы смены в часах
#         total_arrival_lateness = (shift.start_time - shift.arrival_time.time()).seconds / 60  # Опоздание на работу в минутах
#         total_departure_early = (shift.departure_time.time() - shift.end_time).seconds / 60  # Уход раньше смены в минутах
#         total_earned_amount = total_work_hours * employee.hourly_rate  # Итоговая заработанная сумма за смену
#
#         # Суммируем значения для каждого сотрудника
#         if employee.user.username in report_data:
#             report_data[employee.user.username]['total_work_hours'] += total_work_hours
#             report_data[employee.user.username]['total_arrival_lateness'] += total_arrival_lateness
#             report_data[employee.user.username]['total_departure_early'] += total_departure_early
#             report_data[employee.user.username]['total_earned_amount'] += total_earned_amount
#         else:
#             report_data[employee.user.username] = {
#                 'employee_name': employee.fio,
#                 'total_work_hours': total_work_hours,
#                 'total_arrival_lateness': total_arrival_lateness,
#                 'total_departure_early': total_departure_early,
#                 'total_earned_amount': total_earned_amount,
#             }
#
#     return report_data


# tasks.py
# from celery import shared_task
# from django.db.models import Sum
# from datetime import timedelta, datetime
# from .models import Employee, Shift, Attendance, Report
#
#
# @shared_task
# def generate_report():
#     # Получаем дату воскресенья текущей недели
#     sunday = datetime.now().date() - timedelta(days=datetime.now().weekday() + 1)
#
#     # Получаем список сотрудников и их смены за текущую неделю
#     employees = Employee.objects.all()
#     shifts = Shift.objects.filter(day__gte=sunday)
#
#     # Формируем отчет для каждого сотрудника
#     for employee in employees:
#         # Получаем количество отработанных часов за неделю
#         total_hours = timedelta()
#         for day in range(0, 7):
#             shift_start = datetime.combine(sunday + timedelta(days=day), employee.shifts.filter(day=Shift.DAYS[day][0]).first().start_time)
#             shift_end = datetime.combine(sunday + timedelta(days=day), employee.shifts.filter(day=Shift.DAYS[day][0]).first().end_time)
#             attendance = Attendance.objects.filter(shift__employee=employee, shift__day=Shift.DAYS[day][0], arrival_time__gte=shift_start, departure_time__lte=shift_end)
#             total_hours += attendance.aggregate(Sum('departure_time' - 'arrival_time'))['departure_time__sum'] or timedelta()
#
#         # Получаем количество опозданий за неделю
#         late_arrival = timedelta()
#         for day in range(0, 7):
#             shift_start = datetime.combine(sunday + timedelta(days=day), employee.shifts.filter(day=Shift.DAYS[day][0]).first().start_time)
#             attendance = Attendance.objects.filter(shift__employee=employee, shift__day=Shift.DAYS[day][0], arrival_time__gt=shift_start)
#             late_arrival += attendance.aggregate(Sum('arrival_time' - shift_start))['arrival_time__sum'] or timedelta()
#
#         # Получаем количество уходов раньше смены за неделю
#         early_leaving = timedelta()
#         for day in range(0, 7):
#             shift_end = datetime.combine(sunday + timedelta(days=day), employee.shifts.filter(day=Shift.DAYS[day][0]).first().end_time)
#             attendance = Attendance.objects.filter(shift__employee=employee, shift__day=Shift.DAYS[day][0], departure_time__lt=shift_end)
#             early_leaving += attendance.aggregate(Sum(shift_end - 'departure_time'))['departure_time__sum'] or timedelta()
#
#         # Вычисляем заработную плату за неделю
#         rate = employee.rate or 0
#         amount_earned = total_hours.seconds / 3600 * rate
#
#         # Сохраняем отчет в базу данных
#         report = Report(employee=employee, week_start_day=sunday, week_end_day=sunday + timedelta(days=6), hours_worked=total_hours, rate=rate, late_arrival=late_arrival.seconds // 60, early_leaving=early_leaving.seconds // 60, amount_earned=amount_earned)
#         report.save()
#