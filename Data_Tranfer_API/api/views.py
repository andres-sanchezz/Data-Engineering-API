from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .utils import validate_department, validate_employee, validate_job
from .models import Departments, Hired_Employee, Jobs
import json


class CompanyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, table='hired_employees'):
        if table == 'departments':
            model = Departments
        elif table == 'jobs':
            model = Jobs
        elif table == 'hired_employees':
            model = Hired_Employee
        else:
            return JsonResponse({
                'message': 'Table not found'
            })

        return JsonResponse({
            'message': 'Success',
            'data': list(model.objects.all().values())
        })

    def post(self, request):
        json_data = json.loads(request.body)

        table = json_data['destination_table']
        data = json_data['data']

        if table == 'department':
            batch = [Departments(id=d['id'], department=d['department']) for d in data if validate_department(d)]
            Departments.objects.bulk_create(batch)
        elif table == 'jobs':
            batch = [Jobs(id=d['id'], job=d['job']) for d in data if validate_job(d)]
            Jobs.objects.bulk_create(batch)
        elif table == 'hired_employees':
            batch = [
                Hired_Employee(id=d['id'], 
                               name=d['name'],
                               datetime=d['datetime'],
                               department_id=Departments.objects.get(id=d['department_id']),
                               job_id=Jobs.objects.get(id=d['job_id'])
                ) 
                for d in data
                if validate_employee(d)
            ]
            Hired_Employee.objects.bulk_create(batch)
        else:
            response = {'message': 'Table not found...'}

            return JsonResponse(response)

        response = {'message': 'Success. Inserted ' + str(len(batch)) + ' items out of ' + str(len(data))}

        return JsonResponse(response)


    def put(self, request):
        pass

    def delete(self, request):
        pass