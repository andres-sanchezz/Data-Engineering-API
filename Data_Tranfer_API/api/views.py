from django.shortcuts import render

from unicodedata import name
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Company
import json


class EmployeeView(View):
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        pass

    def post(self, request):
        json_data = json.loads(request.body)

    def put(self, request):
        pass

    def delete(self, request):
        pass