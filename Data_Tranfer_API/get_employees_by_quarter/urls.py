from django.urls import path
from .views import EmployeesByQuarterView

urlpatterns = [
    path('select/', EmployeesByQuarterView.as_view(), name='employees_by_quarter')
]