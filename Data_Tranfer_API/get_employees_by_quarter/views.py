from django.shortcuts import render

from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import json
import pandas as pd
import sys
from sqlalchemy import create_engine
import pymysql

from .rds_config import *

rds_host  = "apidb.cisebersdotq.us-east-1.rds.amazonaws.com"
name = db_username
password = db_password
db_name = db_name

class EmployeesByQuarterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            conn = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(name, password, rds_host, db_name))
        except pymysql.MySQLError as e:
            sys.exit()

        data_emp = pd.read_sql('''SELECT 
                                    dep.department, 
                                    job.job, 
                                    SUM(CASE WHEN QUARTER(emp.datetime) = 1 THEN 1 ELSE 0 END) Q1, 
                                    SUM(CASE WHEN QUARTER(emp.datetime) = 2 THEN 1 ELSE 0 END) Q2, 
                                    SUM(CASE WHEN QUARTER(emp.datetime) = 3 THEN 1 ELSE 0 END) Q3, 
                                    SUM(CASE WHEN QUARTER(emp.datetime) = 4 THEN 1 ELSE 0 END) Q4
                                FROM Company_db.api_hired_employee emp
                                JOIN Company_db.api_departments dep
                                ON emp.department_id_id = dep.id
                                LEFT JOIN Company_db.api_jobs job
                                ON emp.job_id_id = job.id
                                WHERE YEAR(emp.datetime) = 2021
                                GROUP BY dep.department, job.job
                                ORDER BY dep.department, job.job''', conn)

        return JsonResponse({'Data':data_emp.to_string()})