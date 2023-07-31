from datetime import datetime

from django.forms import TimeInput, formset_factory
from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ShiftCreateForm
from .models import Employee, Shift, Attendance, Report


# class ScheduleListView(ListView):
#     template_name = "coffeeshop/employees_schedule_details.html"
#     model = Shift
#     context_object_name = "schedule"


class LogoutView(LogoutView):
    next_page = reverse_lazy('coffeeshop:login')


class EmployeesListView(LoginRequiredMixin, ListView):
    template_name = "coffeeshop/employees_list.html"
    queryset = (
        Employee.objects
        .select_related('user')
    )
    context_object_name = "employees"


class ScheduleListView(ListView):
    template_name = "coffeeshop/employees_schedule_details.html"
    # queryset = (
    #     Shift.objects.select_related('employee')
    # )
    model = Shift
    context_object_name = "schedule"

    def get_queryset(self):
        employee_id = self.kwargs.get('pk')
        employee = get_object_or_404(Employee, id=employee_id)
        self.employee = employee
        return super().get_queryset().filter(employee=employee)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.employee
        return context


class ScheduleCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Shift
    fields = "employee", "day", "start_time", "end_time"
    context_object_name = "schedule"
    template_name = "coffeeshop/schedule_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_time'].widget = TimeInput(format='%H:%M')
        form.fields['end_time'].widget = TimeInput(format='%H:%M')
        return form

    def get_success_url(self):
        employee = self.object.employee
        return reverse('coffeeshop:schedule', kwargs={"pk": employee.pk}, )


class ScheduleUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Shift
    fields = "employee", "day", "start_time", "end_time"
    template_name = 'coffeeshop/schedule_update_form.html'
    context_object_name = "schedule"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('shift_id', None)
        if pk is not None:
            return self.model.objects.get(pk=pk)
        else:
            return super().get_object(queryset)

    def get_success_url(self):
        employee = self.object.employee
        return reverse('coffeeshop:schedule', kwargs={"pk": employee.pk}, )


class ScheduleDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Shift
    template_name = 'coffeeshop/schedule_confirm_delete.html'
    context_object_name = "schedule"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('shift_id', None)
        if pk is not None:
            return self.model.objects.get(pk=pk)
        else:
            return super().get_object(queryset)

    def get_success_url(self):
        employee = self.object.employee
        return reverse('coffeeshop:schedule', kwargs={"pk": employee.pk}, )


class ShiftCreateView(CreateView):

    model = Attendance
    template_name = "coffeeshop/mark_shift.html"
    form_class = ShiftCreateForm

    # def get_queryset(self):
    #     employee_id = self.kwargs.get('pk')
    #     employee = get_object_or_404(Employee, id=employee_id)
    #     self.employee = employee
    #     return super().get_queryset().filter(employee=employee)

    def get_success_url(self):
        # employee = self.object.employee
        # return reverse('coffeeshop:schedule', kwargs={"pk": employee.pk}, )
        return reverse('coffeeshop:employees_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employee_id'] = self.kwargs['pk']
        kwargs['shift_id'] = self.kwargs.get('shift_id')
        return kwargs

    # def form_valid(self, form):
    #     attendance = form.save(commit=False)
    #     attendance.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        shift_id = self.kwargs.get('shift_id')

        attendance = Attendance.objects.filter(shift=shift_id).first()

        if attendance:
            attendance.departure_time = datetime.now()
            attendance.save()
        else:
            attendance = form.save(commit=False)
            attendance.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(id=self.kwargs['pk'])
        context['shift'] = Shift.objects.get(id=self.kwargs.get('shift_id'))
        return context

    def get(self, request, *args, **kwargs):
        if 'shift_id' not in self.kwargs:
            return HttpResponseRedirect(reverse('coffeeshop:employees_list'))
        return super().get(request, *args, **kwargs)


def weekly_report_view(request):
    # Получаем список всех сотрудников и их отчетов из базы данных
    employees = Employee.objects.all()

    # Передаем список сотрудников и их отчетов в шаблон для отображения
    return render(request, 'coffeeshop/weekly_report.html', {'employees': employees})