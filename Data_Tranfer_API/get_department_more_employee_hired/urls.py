from django.urls import path
from .views import DepartmentMoreEmployeeHired

urlpatterns = [
    path('select/', DepartmentMoreEmployeeHired.as_view(), name='department_more_employee_hired')
]