# Generated by Django 4.2.2 on 2023-07-21 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coffeeshop', '0003_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start_day', models.DateField(verbose_name='Начальный день')),
                ('week_end_day', models.DateField(verbose_name='Конечный день')),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Всего часов отработано')),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Ставка в час')),
                ('late_arrival', models.IntegerField(default=0, verbose_name='Утренние опоздания')),
                ('early_leaving', models.IntegerField(default=0, verbose_name='Вечерний уход раньше смены')),
                ('amount_earned', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Итоговая заработанная сумма')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffeeshop.employee', verbose_name='Работник')),
            ],
        ),
    ]
