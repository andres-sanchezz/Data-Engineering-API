from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import sys
from sqlalchemy import create_engine
import pymysql

from .rds_config import *

rds_host  = "apidb.cisebersdotq.us-east-1.rds.amazonaws.com"
name = db_username
password = db_password
db_name = db_name

class DepartmentMoreEmployeeHired(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            conn = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(name, password, rds_host, db_name))
        except pymysql.MySQLError as e:
            sys.exit()

        data_emp = pd.read_sql('''SELECT 
                                    dep_id dep_id,
                                    dep.department department, 
                                    count
                                FROM (
                                    SELECT department_id_id dep_id, COUNT(id) count
                                    FROM Company_db.api_hired_employee
                                    WHERE YEAR(datetime) = 2021
                                    GROUP BY dep_id
                                ) AS emp
                                JOIN Company_db.api_departments dep
                                ON emp.dep_id = dep.id
                                HAVING count > (SELECT AVG(count) FROM (SELECT department_id_id dep_id, COUNT(id) count
                                                                        FROM Company_db.api_hired_employee
                                                                        WHERE YEAR(datetime) = 2021
                                                                        GROUP BY dep_id) AS aux)
                                ORDER BY dep_id, department;''', conn)

        return JsonResponse({'Data':data_emp.to_string()})