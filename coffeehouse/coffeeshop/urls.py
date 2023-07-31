from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

from .views import EmployeesListView, ScheduleListView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView, LogoutView, ShiftCreateView, weekly_report_view

app_name = "coffeeshop"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="coffeeshop/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("employees/", EmployeesListView.as_view(), name="employees_list"),
    path('employees/<int:pk>/', ScheduleListView.as_view(), name="schedule"),
    path('employees/schedule/create', ScheduleCreateView.as_view(), name="schedule_create"),
    path('employees/<int:pk>/<int:shift_id>/update', ScheduleUpdateView.as_view(), name="schedule_update"),
    path('employees/<int:pk>/<int:shift_id>/delete', ScheduleDeleteView.as_view(), name="schedule_delete"),

    path('employees/<int:pk>/<int:shift_id>/mark/', ShiftCreateView.as_view(), name="mark"),
    path('report/', weekly_report_view, name="report"),
]
