from datetime import datetime
from croniter import croniter

from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Работник')
    fio = models.CharField(max_length=100, null=False, blank=True, verbose_name='ФИО')
    position = models.CharField(max_length=50, null=False, blank=True, verbose_name='Должность')
    weekly_report = models.JSONField(null=True, blank=True, verbose_name='Еженедельный отчет')

    def __str__(self):
        return self.fio or self.position


class Shift(models.Model):
    DAYS = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    day = models.CharField(max_length=12, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Attendance(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, verbose_name="Смена")
    arrival_time = models.DateTimeField(auto_now_add=True, verbose_name="Время прихода")
    departure_time = models.DateTimeField(auto_now=True, verbose_name="Время ухода")


class Report(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Работник")
    week_start_day = models.DateField(verbose_name="Начальный день")
    week_end_day = models.DateField(verbose_name="Конечный день")
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Всего часов отработано")
    rate = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Ставка в час")
    late_arrival = models.IntegerField(default=0, verbose_name="Утренние опоздания")
    early_leaving = models.IntegerField(default=0, verbose_name="Вечерний уход раньше смены")
    amount_earned = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Итоговая заработанная сумма")
