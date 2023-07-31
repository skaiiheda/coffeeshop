from django.contrib import admin
from .models import Employee, Shift, Attendance
from django.contrib import admin


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = "user", "fio", "position"

    def get_queryset(self, request):
        return Employee.objects.select_related("user")


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = "employee_verbose", "day", "start_time", "end_time"

    def get_queryset(self, request):
        return Shift.objects.select_related("employee")

    def employee_verbose(self, obj: Shift) -> str:
        return obj.employee.fio or obj.employee.position


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = "shift_verbose", "arrival_time", "departure_time"

    def get_queryset(self, request):
        return Attendance.objects.select_related("shift")

    def shift_verbose(self, obj: Attendance) -> str:
        return obj.shift.day
