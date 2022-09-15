from django.urls import path
from .views import CompanyView

urlpatterns = [
    path('employees/', CompanyView.as_view(), name='employees_post'),
    path('employees/<str:table>', CompanyView.as_view(), name='employees_get')
]